# Simple Harmonic Motion
# 110.10.31

from vpython import*

g = 9.8
size, m = 0.05, 0.2
L, K = 0.5, 15 # L:彈簧長度
scene = canvas(width = 500, hwight = 500, center = vec(0, -0.2, 0), background = vec(0.5, 0.5, 0))
ceiling = box(length = 0.8, height = 0.005, width = 0.8, color = color.blue)
ball = sphere(radius = size, color = color.red)
spring = helix(radius = 0.02, thickness = 0.01) # default pos = (0,0,0)
ball.v = vec(0, 0, 0)
ball.pos = vec(0, -L, 0)
dt = 0.001
while True:
    rate(1000)
    spring.axis = ball.pos - spring.pos # extend from spring endpoint to ball
    spring_force = -K*(mag(spring.axis)-L) * spring.axis.norm() # get spring force vector
    ball.a = vector(0, -g, 0) + spring_force/m

    ball.v += ball.a*dt
    ball.pos += ball.v*dt

