import math
k1 = 0.5
k2 = 0.1
q1=0
q2=0
q0=0
eo2 = 3.3
eo1 = 1.2
eo0 = 1.2
for i in range(0,30):
    tq2 = q2
    tq1 = q1
    tq0 = q0
    q2 = k1*(eo1-eo2)+k2*(tq1-tq2)
    q1 = k1*(eo2-eo1)+k2*(tq2-tq1) + k1*(eo0-eo1)+k2*(tq0-tq1)
    q0 = k1*(eo1-eo0)+k2*(tq1-tq0)
    #q0 = 0.5*sq1+(eo1-eo0)
    print(q0,q1,q2)
print(q0+q1+q2)
