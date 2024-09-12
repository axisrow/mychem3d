import math
q =[0.0,0.0,0.0,0.0,0.0,0.0,0.0]
N = len(q)
w = [3.44,2.55,2.55,3.44,2.55,2.55,3.44]
k1 = 0.25
k2 = 0.2
for n in range(0,1000):
    tq = q.copy()
    for i in range(1,N-1):
        q[i] = k1*(w[i+1]-w[i])+k2*(tq[i+1]-tq[i]) + k1*(w[i-1]-w[i])+k2*(tq[i-1]-tq[i])
    q[0]= k1*(w[1]-w[0])+k2*(tq[1]-tq[0])
    q[N-1]= k1*(w[N-2]-w[N-1])+k2*(tq[N-2]-tq[N-1])
    print(q)
print(sum(q))