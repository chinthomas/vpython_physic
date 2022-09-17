# 
# 110.10.31

from vpython import*

size = [0.05, 0.04]
mass = [0.2, 0.4]
colors =[color.yellow, color.red]
position = [vec(0, 0, 0), vec(0.2, -0.35, 0)]
velocity = [vec(0, 0, 0), vec(-0.2, 0.30, 0)]

scene = canvas(width = 800, height = 800, center = vec(0, -0.2, 0), background = vec(0.5, 0.5, 0))
ball_reference = sphere(pos = vec(0, 0, 0), radius = 0.02, color = color.green)

def af_col_v(m1, m2, v1, v2, x1, x2): # function after collision
    v1_prime = v1 + 2* (m2/(m1+m2))*(x1-x2)  * dot(v2-v1, x1-x2) / dot(x1-x2, x1-x2) # dot:兩數相乘
    v2_prime = v2 + 2* (m1/(m1+m2))*(x2-x1)  * dot(v1-v2, x2-x1) / dot(x2-x1, x2-x1) ### 公式???
    return (v1_prime, v2_prime)

# collision formula 二維碰撞
def collision_2(m1, m2, v1, v2, x1, x2): # function after collision
    v1_x, v2_x = collision_1((x1-x2) * dot(v2-v1, x1-x2) / dot(x1-x2, x1-x2), (x2-x1) * dot(v1-v2, x2-x1) / dot(x2-x1, x2-x1),m1,m2)
    v1_y = v1 - (x1-x2) * dot(v2-v1, x1-x2) / dot(x1-x2, x1-x2)
    v2_y = v2 - (x2-x1) * dot(v1-v2, x2-x1) / dot(x2-x1, x2-x1)
    
    return (v1_x + v1_y, v2_x + v2_y)

def collision_1(v1, v2, m1=1, m2=1):
    v1_after = (m1-m2)/(m1+m2) * v1 + 2*m2/(m1+m2) * v2
    v2_after = 2*m1/(m1+m2) * v1 + (m1-m2)/(m1+m2) * v1
    return (v1_after, v2_after)
# 設定兩顆球的樣式
balls=[]
for i in range(2):
    balls.append(sphere(pos = position[i], radius = size[i], color = colors[i]))
    balls[i].v = velocity[i]
    balls[i].m = mass[i]

dt = 0.001

while True:
    rate(1000)

    for ball in balls:
        ball.pos += ball.v * dt
    
    if (mag(balls[0].pos - balls[1].pos) <= size[0] + size [1] and dot(balls[0].pos - balls[1].pos, balls[0].v - balls[1].v) <= 0):
        (balls[0].v, balls[1].v) = collision_2(balls[0].m, balls[1].m, balls[0].v, balls[1].v, balls[0].pos, balls[1].pos)
