from vpython import*

g = 9.8
size = 0.25
height = 15.0
C_drag = 1.2

scene = canvas(width = 600, height = 600 ,center = vec(0, height / 2, 0))
floor = box(length = 30, height = 0.01, width = 10, color = color.blue )
ball = sphere(radius = size, color = color.red, make_trail = True, trail_radius = size)
ball.pos = vec(-15, size, 0)
ball.v = vec(16, 16, 0)

dt = 0.001
while ball.pos.y >= size:
    rate(1000)
    ball.v += vec(0, -g, 0) * dt - C_drag * ball.v *dt
    ball.pos += ball.v*dt
msg = text(text = 'final speed = ' + str(ball.v.mag), pos = vec(-10, 15, 0))
