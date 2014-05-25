
T = 0
N = 0

def om(S, W, R):
    global T
    global N
    
    if R == 0:
        N = N + 1
        print N, W, T, S
        T = T + W
    else:
        om(S + "0", W, R-1)
        om(S + "1", W, R-1)
        
for i in range(1,5):        
    om("", i, i)
