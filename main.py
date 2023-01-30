# Generating pdf of state

pdf_store = {}
# Storing values
def pdf(a, b, n = 1000):
    if (a, b, n) in pdf_store:
        return pdf_store[(a,b,n)]
    
    else:
        out = {}
        s = 0
        c = 0

        for i in range(a, n-b+1):
            start = 1
            for j in range(0, a):
                start = start*((i-j)/(n-j))

            for k in range(0, b):
                start = start*((n-i-k)/(n-a-k))
            out[i] = start
            s+=start
            c+=1
        out = {x: out[x]/s for x in out}
        m = sum([out[x]*(x-a) for x in out])
        pdf_store[(a,b,n)] = [out, m]
        return [out, m]

# Calculating Loss Function. Do NOT enter n <= 0

loss_store = {}

def loss(a, b, c, d, n = 1000):
    if (a,b,c,d,n) in loss_store:
        return loss_store[(a,b,c,d,n)]

    else:
        # Suppose bags start with n candies. a, b are the sweet/sour candies of bag 1, c, d are sweet/sour candies of bag 2
        A, B = pdf(a,b,n), pdf(c, d, n)
        if A[1]-a < B[1]-c:
            L = loss(c, d, a, b, n)
            return [L[0], L[2], L[1]]
        
        else:
            # Loss 1: If we were to pick the better bag now
            # Loss 2: If we look at one more candy in bag 1 (better bag)
            # Loss 3: If we look at one more candy in bag 2 
            
            
            L0, L1, L2 = 0, 0, 0
            
            for r in range(a, n-b+1):
                
                for s in range(r+c, (n-d)+1):
                    
                    L0 += A[0][r]*B[0][s]*(s-c-r+a)
                    
                    L2 += A[0][r]*B[0][s]*(s-c)
                    
                    
                for s in range(c, min((n-d), c+r)+1):
                    
                    L1 += A[0][r]*B[0][s]*(r-a)
            
            if c+d != n:
                L2 = L2/(n-c-d)
            else:
                L2 = n
                
            if a+b != n:
                L1 = L1/(n-a-b)
            else:
                L1 = n
            loss_store[(a, b, c, d, n)] = [L0, L1, L2]
            return [L0, L1, L2]

import random
def game_sim(n = 1000):
    a_sweet, b_sweet = random.randint(0, n), random.randint(0, n)
    A, B = [1]*a_sweet + [0]*(n-a_sweet), [1]*b_sweet + [0]*(n-b_sweet)
    random.shuffle(A)
    random.shuffle(B)

    a_pos, b_pos = 0, 0
    x, y, z, w = 0, 0, 0, 0
    
    while True:
        
        L = loss(x, y, z, w, n)    
        M = min(L)
        
        if L[0] == M:
            break
        elif L[1] == M:
            
            # Draw m 
            m = min(n - a_pos, max(1, int(L[2]/L[1]))) if L[1] != 0 else 1
            for j in range(a_pos, a_pos+m):
                if A[j] == 1:
                    x += 1
                else:
                    y += 1
            a_pos += m
            
            
        elif L[2] == M:
            # Draw m 
            m = min(n - b_pos, max(1, int(L[1]/L[2]))) if L[2] != 0 else 1
            for j in range(b_pos, b_pos+m):
                if B[j] == 1:
                    z += 1
                else:
                    w += 1
            b_pos += m
            
            
            
    if pdf(x, y, n)[1] - x >= pdf(z, w, n)[1] - z:
        return a_sweet - x, a_sweet >= b_sweet, x+y, a_sweet, b_sweet
    
    else:
        return b_sweet - z, b_sweet >= a_sweet, z+w, a_sweet, b_sweet


out = {}
boo = 0
count = 0

N = 10000

for i in range(N):
    A = game_sim()
    print(A)
    
    if A[0] in out:
        out[A[0]] += 1

    else:
        out[A[0]] = 1

    if A[1] == False:
        boo += 1


    count+=A[2]

    if i % 1000 == 0:
        print(i, N)

print(sum([out[x]*x for x in out])/N)
print(boo/N, count/N)
print(sum(out.values()))
