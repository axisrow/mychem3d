import glm

a = glm.vec4(0,0,0,1)
#a.w = 0
print(a.to_bytes())
print(a)
b = glm.vec4(0,0,0,1)
#print(a/2)


#vec4 qmul(vec4 q1, vec4 q2)
#{
         #return vec4(
             #q2.xyz * q1.w + q1.xyz * q2.w + cross(q1.xyz, q2.xyz),
             #q1.w * q2.w - dot(q1.xyz, q2.xyz)
         #);
#}

def qmul(q1,q2):
    return glm.vec4 ( q2.xyz * q1.w + q1.xyz * q2.w + glm.cross(q1.xyz, q2.xyz),  q1.w * q2.w)
    

print (qmul(a,b))
print( a*b)



