from vpython import*
import numpy as np


N = 50          # the number of balls
A = 0.01        # amplitude
m, k, d = 0.1, 10.0, 0.4 # mass of ball, 彈力常數, length between balls

# 做圖設定
PDR = graph(title = 'Phonon Dispersion Relation', width=800, height = 300, align='center', background = vec(0.6, 0.7, 0.95))
func1 = gcurve(graph=PDR, color=color.red, width=4)


for n in range(1, N//2-1):
    rate(10000)
    # n*wavelegth(N*d) = 2*pi
    # 初始位置為SIN 函數圖形
    wavefactor = 2*pi*n / (N*d) 
    phase = wavefactor * arange(N) * d 
    ball_pos, ball_orig, ball_v, spring_len = np.arange(N)*d + A*np.sin(phase), np.arange(N)*d, np.zeros(N), np.ones(N)*d
    t, dt = 0, 3E-4
    
    while ball_pos[1] - ball_orig[1] >= 0:
        
        t += dt
        spring_len[:-1] = ball_pos[1:N] - ball_pos[:N-1]
        spring_len[-1] = ball_pos[0] + N*d - ball_pos[-1]
        ball_v[1:] += k*(spring_len[1:]-d)/m*dt - k*(spring_len[:N-1]-d)/m*dt
        ball_pos += ball_v*dt
    # 
    func1.plot(pos = (wavefactor, pi / t / 2))