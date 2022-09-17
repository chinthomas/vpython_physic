#2021.10.07

from vpython import*
g = 9.8
size = 0.25
height = 15.0

#canvas() : opens a window name scene
#.center : the position vector of the center of the simulation world
#.background : set background color(rgb)
scene = canvas(width = 800, height = 800, center = vec(0,height/2,0),background = vec(0.5,0.5,0))

#box() : create a box call floor
floor = box(lenght = 30, height = 0.1, width = 10 , color = color.blue)

#make_trail : draw a trail for the object
#trail_radius : the thickness of the trail
ball = sphere(radius = size, color = color.red, make_trail = True, trail_radius = 0.05)

#test() : show message
msg = text(text = 'Free Fall', pos = vec(-10,10,0))

ball.pos = vec(0, height, 0)
ball.v = vec(0,0,0)

dt = 0.001 #time step

while ball.pos.y >= size:
    rate(1000)  #run 1000 times per real second

    ball.pos = ball.pos + ball.v*dt
    ball.v.y = ball.v.y - g*dt

msg.visible = False
msg = text(text = str(ball.v.y),pos = vec(-10,0,0))
print(ball.v.y)
