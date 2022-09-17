##############################
# vpython homework 2
# last revise : 2021 / 10 / 20 
##############################
'''
Homework:
write a program for Newton’s cradle with 5 balls. The dimensions of the cradle and the initial conditions, in 
which all balls are at rest, are shown in the figure below. The mass of each ball is 1kg, and the radius of each 
ball is 0.2m and the distance between any two adjacent pivots are 0.4m.  The program need to have a variable 
N that indicates how many balls are lifted at the beginning, for example in the figure N=2. In the program, 
also use dt, k, g = 0.0001, 150000, vector(0,-9.8,0) for the time step of the simulation, the force constant of 
the rope, and the gravitation acceleration, respectively. And the simulation is set at rate(5000). 
Also (1) In one graph, plot versus time both the total of the instant kinetic energies of all balls, and the total 
of the instant gravitational potential energy of all balls (the potential energy of the balls at the lowest 
positions are taken to be 0). (2) In a second graph, plot versus time the averaged total kinetic energy over 
the time period (from the beginning of the simulation till the time of the current plot point) and the averaged 
total gravitational potential energy. 
''' 

from vpython import*

### the background ###
N = 2                    # the balls are lifted
g = vector(0,-9.8,0)     # g = 9.8m/s^2
m = 1                    # mass = 1KG 
size = 0.2               # ball radius = 0.2 meter
dt, k = 0.0001, 150000
L = 2 - m*mag(g)/k       # rope origin length
scene = canvas(width = 800, height = 400, center = vec(0, -1, 0), background = vec(0.6, 0.7, 0.98))

### the object ###
pivots = []
balls = []
ropes = []
for i in range(5):
    pivot = sphere(radius = 0.05, pos = vec((i-2)*0.4, 0, 0), color = color.black)
    pivots.append(pivot)

    ball = sphere(radius = size, pos = vec((i-2)*0.4, -2.0, 0), color = color.orange)
    ball.v = vector(0, 0, 0)
    balls.append(ball)

    rope = cylinder(pos = vec((i-2)*0.4, 0, 0), radius = 0.03, color = color.orange)
    rope.axis = vector(0, -2, 0)
    ropes.append(rope)

### collision ###    
# collision origin
def af_col_v( v1, v2, x1, x2, m1=1, m2=1): # function after collision
    v1_prime = v1 + 2* (m2/(m1+m2))*(x1-x2)  * dot(v2-v1, x1-x2) / dot(x1-x2, x1-x2) # dot:兩數相乘
    v2_prime = v2 + 2* (m1/(m1+m2))*(x2-x1)  * dot(v1-v2, x2-x1) / dot(x2-x1, x2-x1) ### 公式???
    return (v1_prime, v2_prime)

# collision formula 二維碰撞
'''
def collision_2(v1, v2, x1, x2): # function after collision
    v1_x, v2_x = collision_1((x1-x2) * dot(v2-v1, x1-x2) / dot(x1-x2, x1-x2), (x2-x1) * dot(v1-v2, x2-x1) / dot(x2-x1, x2-x1))
    v1_y = v1 - (x1-x2) * dot(v2-v1, x1-x2) / dot(x1-x2, x1-x2)
    v2_y = v2 - (x2-x1) * dot(v1-v2, x2-x1) / dot(x2-x1, x2-x1)
    
    return (v1_x + v1_y, v2_x + v2_y)

def collision_1(v1, v2, m1=1, m2=1):
    v1_after = (m1-m2)/(m1+m2) * v1 + 2*m2/(m1+m2) * v2
    v2_after = 2*m1/(m1+m2) * v1 + (m1-m2)/(m1+m2) * v1
    return (v1_after, v2_after)'''

### the graph and function ###
E_instant = graph(width = 400, align = 'left')
E_average = graph(width = 400, align = 'left')

func_K_i = gdots(graph = E_instant, color = color.yellow, size = 1)
func_U_i = gdots(graph = E_instant, color = color.red, size = 1)

func_K_a = gdots(graph = E_average, color = color.yellow, size = 1)
func_U_a = gdots(graph = E_average, color = color.red, size = 1)
K_i, U_i, K_a, U_a = 0, 0, 0, 0

########################## stimulation ###############################
### lift N balls up 0.05m ###
x = sqrt(2**2 -1.95**2) # ball go to left
for i in range(N):
    balls[i].pos += vector(-x, 0.05, 0)
    ropes[i].axis = balls[i].pos - pivots[i].pos

### balls become moving ###
t = 0
while True:
    rate(5000)
    t += dt
   
    ### ball dropping
    for i in range(5):
        rope_force = -k*(mag(ropes[i].axis) - L)* ropes[i].axis.norm()
        balls[i].a = g + rope_force/m
        balls[i].v += balls[i].a*dt
        balls[i].pos += balls[i].v*dt
        ropes[i].axis = balls[i].pos - pivots[i].pos
    
    ### collision start
    for i in range(4):
        if mag(balls[i].pos - balls[i+1].pos) <= 0.4 and balls[i].v.x - balls[i+1].v.x > 0 :
            (balls[i].v, balls[i+1].v) = af_col_v(balls[i].v, balls[i+1].v, balls[i].pos, balls[i+1].pos)
            #balls[i].v, balls[i+1].v = balls[i+1].v, balls[i].v

    ### draw graphs
    # calculate five balls total instant energy
    K_i, U_i = 0, 0
    for n in range(5):
        K_i += (1/2 * m * mag(balls[n].v)**2)
        U_i += (m * mag(g) * (balls[n].pos.y + 2))
    
    # accumulate total kinetic/potential energy of all time
    K_a += K_i
    U_a += U_i

    # draw function
    func_K_i.plot(pos = (t, K_i))
    func_U_i.plot(pos = (t, U_i))
    func_K_a.plot(pos = (t, K_a/t))
    func_U_a.plot(pos = (t, U_a/t))
            
                      
