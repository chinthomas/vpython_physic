from vpython import*

g = 9.8 
size = 0.25

scene = canvas(center = vec(0,5,0), width = 600, background = vec(0.5,0.5,0))
floor = box(lenght = 30, height = 0.01, width = 4, color = color.blue)
ball = sphere(radius = size, color = color.red, make_trail = True, trail_radius = size / 3)

ball.pos = vec(-15.0, 10.0, 0.0)
ball.v = vec(2.0, 0.0, 0.0)
dt = 0.001

while ball.pos.x < 15.0:
    rate(1000)
    ball.pos+= ball.v * dt
    ball.v.y += -1* g * dt

    if ball.pos.y <= size and ball.v.y < 0:
        ball.v.y *= -1

