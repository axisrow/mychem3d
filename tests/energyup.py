import math

x1 = 0
m1 = 1
v1 = 0.1

x2 = 100
v2 = 0
m2 = 16

t=0
E0 = v1*v1*m1/2 + v2*v2*m2/2
while(1):
    t+=1
    delta = x2-x1
    a=0
    if abs(delta)<10:
        a = -0.1/delta/delta
    v1+=a
    v2+=-a/m2
    v1a = v1
    if v1>1:
         v1 = 1
    if v1<-1:
         v1 = -1

    x1+=v1
    x2+=v2
    E = v1*v1*m1/2 + m2*v2*v2/2
    print(f"t= {t} x1={x1:.2f} v1={v1:.3f} a={a:.3f},  v1a={v1a:.2f},  x2={x2:.2f},v2={v2:.3f} E= {E:.3f}")
    if t%100==0: print(t)
    if x1<0: break
print(f"E0={E0:.3f}, E-E0={ E-E0:.3f}  {(E-E0)/E0*100:.2f}%")

