import glm

q1 = glm.quat()
q2 = glm.quat()
#q1.x = 1

a = glm.array(q1,q2)
q3 = a[0]
print(q3)
q3.x = 1
print(q3)
#print(glm.quat(a[0]))
#print(a)
v1 = glm.vec3(1,0,0)
v2 = glm.vec3(1,0,0)
cr = glm.cross(v1,v2)
print(cr)
print(glm.normalize(cr))
print(v1==v2)