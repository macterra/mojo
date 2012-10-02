import code, random

def binary(x):
    if (x == 1 or x == 0):
        return str(x)
    else:
        return binary(int(x/2)) + str(x % 2)
     

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

rnd = random.Random()

class Action:
    def __init__(self, bits, tape):
        #if True:
        #if rnd.choice([0,1]):
        if tape.peek(): 
            self.output = tape.read()
            self.next = tape.readInt(bits) 
        else:
            self.next = tape.readInt(bits)
            self.output = tape.read()
        
    def __repr__(self):
        return "out: {0} next: {1}".format(self.output, self.next)
        
class TMachine:
    def __init__(self, bits):
        self.bits = bits
        self.size = 2**bits
        self.state = 0
        self.states = []
        
    def read(self, program):
        # an N bit TMachine will read (2**N)*(2N+2) bits from the program to initialize its FSM
        self.states = []        
        print "reading {0} states from {1}".format(self.size, program)        
        program.seek(0)
        
        for i in range(self.size):
            act0 = Action(self.bits, program)
            act1 = Action(self.bits, program)
            self.states.append([act0, act1])        
        
    def execute(self, program, input, steps):
        self.read(program)
        print self.states
        
        self.state = 0        
        input.seek(0)
        output = Tape(1)
        
        for i in range(steps):
            act = self.states[self.state][input.read()]
            # print i, act
            output.write(act.output)
            self.state = act.next
        print "running {0} on {1} yielded {2}".format(program, input, output)
        return output  
            

BITS = 8
SIZE = 2**BITS

tapes = []
freq = [0] * SIZE

for i in range(SIZE):
    tapes.append(Tape(i))
    
#print tapes    

def runMachine(size, programs, inputs):    
    tm = TMachine(size)

    for p in programs:
        for i in inputs:
            output = tm.execute(p, i, BITS)
            freq[int(output)] += 1

runMachine(1, tapes[130:131], tapes)
#runMachine(1, tapes, tapes)
            
for (t, f) in zip(tapes, freq):
    print int(t), t, f
    
#code.interact(local=locals())
            
            
            

    
