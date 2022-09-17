################################################
# vpython homework 1
# 2021-10-12
################################################
'''
A  ball,  whose  radius  is  size  =  0.25,  at  initial  position  =  vec(-15,  size,  0),  with  initial  velocity  ball.v  = 
vec(20*cos(theta), 20*sin(theta), 0) and theta = pi/4, is launched with a linear air drag of drag Coefficient 
C_drag = 0.9 . When the ball hits the ground, it bounces elastically.  
(1) Plot the trajectory of the ball and stop the ball when it hits the ground for 3 times. Also add at the center 
of the ball an arrow, which moves along with the ball and whose length is proportional (proportional 
constant by your choice) to and parallel to the velocity vector of the ball.  
(2) Plot a graph of speed (magnitude of the velocity) of the ball versus time.  
(3) Show both the displacement of the ball and the total distance travelled by the ball. Note: in python, x**p 
means x to the power p = x p . 
(4) Show the largest height of the ball during the entire process.  
'''

from vpython import*

g = 9.8         # g = 9.8 m/(s^2)
size = 0.25     # the size of ball
C_drag = 0.9    # drag Coefficient = 0.9
theta = pi / 4
dt = 0.001
t = 0           #  total time
hit_ground = 0  # the number of the ball hits the ground

# the background setting
scene = canvas(align = 'left', width = 600, center = vec(0, 2, 0), background = vec(0.6, 0.75, 0.95))
floor = box(length = 30, width = 4, height = 0.1, color = color.blue)

# initialization of the ball
ball = sphere(radius = size, color = color.red, make_trail = True, trail_radius = size*0.5)
ball.pos = vec(-15, size, 0)
ball.v = vec(20*cos(theta), 20*sin(theta), 0)

velocity = arrow(color = color.black, shafwidth = 0.25)
velocity.pos = ball.pos
velocity.axis = ball.v * 0.5

# the graph and function
speed_time = graph(width = 600, align = 'right')
func1 = gdots(graph = speed_time, color = color.orange, size = 2)

# the data have to know
large_heigth = ball.pos.y       # find the largest height of the ball 
distance = 0                     # the total distance ball have traveled

while hit_ground < 3:
    rate(1000)

    # the motion of the ball and use vector to show the velocity
    ball.v += (vec(0, -g, 0) - ball.v * C_drag) * dt
    ball.pos += ball.v * dt
    velocity.pos = ball.pos
    velocity.axis = ball.v * 0.5

    # draw the graft
    t += 0.001
    func1.plot(pos = (t, ball.v.mag))

    # get the data 1.distance 2. largest height
    distance += ball.v.mag * dt
    if ball.pos.y > large_heigth:
        large_heigth = ball.pos.y
    
    # the ball hit the ground
    if ball.pos.y <= size and ball.v.y <0:
        hit_ground += 1
        ball.v.y *= -1

# show the data we have got on the screen    
message1 = text(text = 'displacement = ' + str(ball.pos.x + 15), pos = vec(-10, -3, 0), color = color.black)   
message2 = text(text = 'total distance = ' + str(distance), pos = vec(-10, -4.5, 0), color = color.black)    
message3 = text(text = 'largest height = ' + str(large_heigth), pos = vec(-10, -6, 0), color = color.black)

