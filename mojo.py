import sys, code, random, math

def binary(s):
    return str(s) if s<=1 else binary(s>>1) + str(s&1)
          
def minBits(n):
    return int(math.ceil(math.log(n,2)))
        
class Tape:
    def __init__(self, x):
        self.init(x)
        
    def __repr__(self):
        return self.tape[::-1]
        
    def __int__(self):
        m = 1
        s = 0
        
        for i in range(self.size()):
            s += self[i] * m
            m *= 2
            
        return s
        
    def __getitem__(self, i):
        if i >= self.size():
            return 0
        else:
            return int(self.tape[i])
            
    def __setitem__(self, i, x):
        s = self.size()
        
        if i >= s:
            if x:
                # extend the tape with enough 0s and add a '1' to the end
                self.tape += '0' * (i - s)
                self.tape += '1'
            return
                        
        self.tape = self.tape[:i] + ('1' if x else '0') + self.tape[i+2:]
        
    def init(self, val):
        self.head = 0
        self.tape = binary(val)[::-1] # reverse of the binary encoding
        
    def clear(self):
        t.init(0)
        
    def seek(self, pos):
        self.head = pos
        
    def normalize(self):
        self.init(int(self))
    
    def size(self):
        return len(self.tape)        
            
    def peek(self):
        return self[self.head]
        
    def read(self):
        bit = self[self.head]
        self.head += 1
        return bit
        
    def write(self, x):
        self[self.head] = x
        self.head += 1
        
    def readInt(self, bits):
        m = 1
        s = 0
        
        for i in range(bits):
            s += self.read() * m
            m *= 2
            
        return s        

    def fixedWidth(self, n):
        s = str(self)
        fill = n - len(s)
        if fill > 0:
            s = "0" * fill + s
        return s    

    def push(self, x):
        self.tape = ('1' if x else '0') + self.tape
        
    def pop(self):
        bit = self[0]
        self.tape = self.tape[1:]
        return bit
        
rnd = random.Random()

class FSAction:
    def __init__(self, bits, tape):
        self.output = tape.read()
        self.next = tape.readInt(bits)
        
    def __repr__(self):
        return "out: {0} next: {1}".format(self.output, self.next)
        
class FSMachine:
    def __init__(self, states):
        self.states = states
        self.bits = minBits(states)
        self.state = 0
        self.actions = []
        
    def programSize(self):
        return 2 * self.states * (self.bits+1)
    
    def read(self, program):
        # an N state FSMachine will read 2N*(bits+1) bits from the program to initialize its FSM
        # where bits is number of bits needed to store N 
        self.actions = []        
        #print "reading {0} states from {1}".format(self.states, program)        
        program.seek(0)
        
        for i in range(self.states):
            act0 = FSAction(self.bits, program)
            act1 = FSAction(self.bits, program)
            self.actions.append([act0, act1])        
        
    def execute(self, program, input, steps):
        self.read(program)
        #print self.actions
        
        self.state = 0        
        input.seek(0)
        output = Tape(0)
        
        for i in range(steps):
            act = self.actions[self.state][input.read()]
            #print i, act
            output.write(act.output)
            self.state = act.next % self.states
        #print "running {0} on {1} yielded {2}".format(program, input, output)
        return output  
     
class StackAction:
    def __init__(self, bits, tape):
        self.output = tape.read()
        self.op = tape.readInt(2)
        self.next = tape.readInt(bits)
        
    def __repr__(self):
        return "<out: {0} op: {1} next: {2}>".format(self.output, self.op, self.next)
        
class StackMachine:
    def __init__(self, states):
        self.states = states
        self.bits = minBits(states)
        
    def reset(self):    
        self.state = 0
        self.actions = []
        self.stack = Tape(0)
        
    def programSize(self):
        return 4 * self.states * (self.bits+3)
        
    def read(self, program):
        # an N state FSMachine will read 2N*(bits+1) bits from the program to initialize its FSM
        # where bits is number of bits needed to store N 
        
        self.reset()
        
        #print "reading {0} states from {1}".format(self.states, program)        
        program.seek(0)
        
        for i in range(self.states):
            act0 = StackAction(self.bits, program)
            act1 = StackAction(self.bits, program)
            act2 = StackAction(self.bits, program)
            act3 = StackAction(self.bits, program)
            self.actions.append([act0, act1, act2, act3])        
        
    def execute(self, program, input, steps):
        self.read(program)
        #print self.actions
        
        self.state = 0        
        input.seek(0)
        output = Tape(0)
        
        for i in range(steps):
            inbit = input.read()
            stbit = self.stack.peek()
            inputs = inbit<<1|stbit
            
            act = self.actions[self.state][inputs]
            #print i, act
            output.write(act.output)
            self.state = act.next % self.states
            
            if act.op == 0:
                pass # no-op
            elif act.op == 1:
                self.stack.pop()
            elif act.op == 2:
                self.stack.push(0)
            elif act.op == 3:
                self.stack.push(1)
                
        #print "running {0} on {1} yielded {2}".format(program, input, output)
        return output  
    
BITS = 8
SIZE = 2**BITS

tapes = []
freq = [0] * SIZE

for i in range(SIZE):
    tapes.append(Tape(i))
    
#print tapes    

def runMachine(size, programs, inputs):    
    fsm = FSMachine(size)

    for p in programs:
        for i in inputs:
            output = fsm.execute(p, i, BITS)
            freq[int(output)] += 1
            
    for (t, f) in zip(tapes, freq):
        print int(t), t, f
        
def runMonteCarlo(machine, N):
    # machine =
    # N = Monte Carlo iterations
    max = 2**machine.programSize()
    bits = minBits(max)
    freq = {}
    rnd = random.Random(0)
    
    for i in range(N):
        program = Tape(rnd.randint(0, max-1))
        input = Tape(rnd.randint(0, max-1))
        output = machine.execute(program, input, bits)
        val = int(output)
        if freq.has_key(val):
            freq[val] += 1
        else:
            freq[val] = 1
        #if (i%10000 == 0): sys.stdout.write('.') 
    
    
    width = int(math.ceil(math.log(max,10)))
    formatstr = "{0:" + str(width) + "d} {1:6.5f} {2:8d} {3}"
    attractors = 0
    
    vals = freq.keys()
    vals.sort()
    
    for i in vals:
        f = freq[i]
        t = Tape(i)
        if f > 1:
            print formatstr.format(i, float(f)/N, f, t.fixedWidth(bits))
            attractors += 1

    hits = len(freq)
    total = max
    misses = max-hits
    print "hits: {0} ({1:.2f}%) misses: {2} ({3:.2f}%) total: {4}".format(hits, 100.*hits/total, misses, 100.*misses/total, total)   
    space = max**2
    print "{0:e} fraction sampled of space {1:e} with {2} samples".format(1.*N/space, space, N)
    print "strangeness {0:.4f} ({1:d} attractors)".format(1.*attractors/max, attractors)
    
def sizeTable():
    for i in range(1,65):
        s = programSize(i)
        print "{0:3d} {1:3d} {2:e}".format(i, s, 2**s)

#sizeTable()
        
#runMachine(4, tapes[254:255], tapes[130:135])
#runMachine(1, tapes, tapes)

#runMonteCarlo(FSMachine(2), 1000)
runMonteCarlo(StackMachine(2), 100000)
              
#code.interact(local=locals())
            
            
            

    
