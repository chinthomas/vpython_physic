import numpy as np
from vpython import*
A, N, omega = 0.1, 50, 2*pi/1.0
size, m, k, d = 0.06, 0.1, 10.0, 0.4

scene = canvas(title = 'Spring Wave', width = 1200, height=450, background = vec(0.5,0.6,0.95), center=vec((N-1)*d/2, 0, 0))
c = curve([vector(i*d, 1.0, 0) for i in range(N)], color=color.black)

Unit_K, n = 2 * pi/(N*d), 5 
Wavevector = n * Unit_K 
phase = Wavevector * arange(N) * d 
ball_pos, ball_orig, ball_v, spring_len = np.arange(N)*d + A*np.sin(phase), np.arange(N)*d, np.zeros(N), np.ones(N)*d
######################################################################
t, dt = 0, 1E-3
while t < 10:
    rate(1000)
    t += dt   
  
    spring_len[:-1] = ball_pos[1:N] - ball_pos[:N-1]
    spring_len[-1] = N*d - ball_pos[-1]
    ball_v[1:] += k*(spring_len[1:]-d)/m*dt - k*(spring_len[:N-1]-d)/m*dt
    ball_v[0] += k*(spring_len[0]-d)/m*dt - k*(spring_len[-1]-d)/m*dt
    ball_pos += ball_v*dt
    
    # 繪製位移曲線
    ball_dist = ball_pos - ball_orig
    for i in range(N):
        c.modify(i, y=ball_dist[i]*4+1)