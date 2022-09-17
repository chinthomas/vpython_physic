#2021.10.07
#show how to use vector


from vpython import*
scene = canvas(width=800, height=800, background=vec(1,0.5,0))

#shaftwidth : 
a1 =arrow(color = color.green, shaftwidth = 0.05)
b1 =arrow(color = color.blue, shaftwidth = 0.05)

a1.pos = vec(1,1,0)
a1.axis = vec(1,-1,0)
b1.pos = a1.pos + a1.axis
b1.axis = vec(2,1,0)

c1 =arrow(color = color.black, shaftwidth = 0.05)
c1.pos = a1.pos
b1.axis = b1.axis + a1.axis
