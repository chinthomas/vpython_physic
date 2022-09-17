# add periodically boundary condition
import numpy as np
from vpython import*
A, N, omega = 0.1, 50, 2*pi/1.0
size, m, k, d = 0.06, 0.1, 10.0, 0.4

scene = canvas(title = 'Spring Wave', width = 1200, height=450, background = vec(0.5,0.6,0.95), center=vec((N-1)*d/2, 0, 0))
balls = [sphere(radius=size, color=color.red, pos=vector(i*d,0,0), v=vector(0,0,0)) for i in range(N)]
spring = [helix(radius=size/2, thickness=d/15, pos=vector(i*d,0,0), axis=vector(d,0,0)) for i in range(N-1)]

# draw a curve on the scene
c = curve([vector(i*d, 1.0, 0) for i in range(N)], color=color.black)

ball_pos, ball_orig, ball_v, spring_len = np.arange(N)*d, np.arange(N)*d, np.zeros(N), np.ones(N)*d 
######################################################################
t, dt = 0, 1E-3
while t < 10:
    rate(1000)
    t += dt
    # add periodically boundary condition
    ball_pos[0] = A* sin(omega*t)
    ball_pos[-1] = ball_pos[0]+(N-1)*d
    spring_len[:-1] = ball_pos[1:N] - ball_pos[:N-1]
    #spring_len[-1] = ball_pos[0] + N*d - ball_pos[-1]
    ball_v[1:] += k*(spring_len[1:]-d)/m*dt - k*(spring_len[:N-1]-d)/m*dt
    #ball_v[0] += k*(spring_len[0]-d)/m*dt - k*(spring_len[-1]-d)/m*dt
    ball_pos += ball_v*dt
    
    # 彈簧合球的運動模型
    for i in range(N): balls[i].pos.x = ball_pos[i]
    for i in range(N-1):
        spring[i].pos = balls[i].pos
        spring[i].axis = balls[i+1].pos - balls[i].pos 
    
    # 繪製位移曲線
    ball_dist = ball_pos - ball_orig
    for i in range(N):
        c.modify(i, y=ball_dist[i]*4+1)


    """ 不用numpy array的方法
    balls[0].pos = vector(A*sin(omega*t), 0, 0)
    for i in range(N-1):
        spring[i].pos = balls[i].pos
        spring[i].axis = balls[i+1].pos - balls[i].pos
    for i in range(1, N):
        if i == N-1: balls[-1].v += -k*vector((spring[-1].axis.mag - d), 0, 0) / m * dt
        else: balls[i].v += k*vector((spring[i].axis.mag - d), 0, 0) / m * dt - k*vector((spring[i-1].axis.mag - d), 0, 0) / m * dt
        balls[i].pos += balls[i].v * dt 
    """