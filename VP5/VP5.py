from vpython import*
from diatomic import*

N = 20                                # 20 molecules
L = ((24.4E-3/(6E23))*N)**(1/3.0)/50  # 2L is the length of the cubic container box, the number is made up
m = 14E-3/6E23                        # average mass of O and C
k, T = 1.38E-23, 298.0                # some constants to set up the initial speed 
initial_v = (3*k*T/m)**0.5            # some constant

scene = canvas(width = 400, height =400, align = 'left', background = vec(1, 1, 1))
container = box(length = 2*L, height = 2*L, width = 2*L, opacity=0.4, color = color.yellow )
energies = graph(width = 600, align = 'left', ymin=0)
c_avg_com_K = gcurve(color = color.green)
c_avg_v_P = gcurve(color = color.red)
c_avg_v_K = gcurve(color = color.purple)
c_avg_r_K = gcurve(color = color.blue) 

COs = list()
for i in range(20):
    O_pos = vec(random()-0.5, random()-0.5, random()-0.5)*L
    CO=CO_molecule(pos = O_pos, axis=vector(1.0*d, 0, 0))
    CO.C.v=vector(initial_v*random(), initial_v*random(), initial_v*random())
    CO.O.v=vector(initial_v*random(), initial_v*random(), initial_v*random())
    COs.append(CO)

sum_data = [0]*4 # com_K, v_K, v_P, and r_K
avg_data = [0]*4 # com_K, v_K, v_P, and r_K
atom = ['C','O']
times=0
dt=5E-16
t=0

while t <100:
    rate(10000)
    for CO in COs:
        CO.time_lapse(dt)

    for i in range(N-1):
        for j in range(i+1, N):
            ## the collisions between the C - C
            if  mag(COs[i].C.pos-COs[j].C.pos) <= 2*size and dot(COs[i].C.pos-COs[j].C.pos, COs[i].C.v-COs[j].C.v) < 0: 
                COs[i].C.v, COs[j].C.v = collision(COs[i].C, COs[j].C)
            ## the collisions between the C - O
            if  mag(COs[i].O.pos-COs[j].C.pos) <= 2*size and dot(COs[i].O.pos-COs[j].C.pos, COs[i].O.v-COs[j].C.v) < 0: 
                COs[i].O.v, COs[j].C.v = collision(COs[i].O, COs[j].C)
            ## the collisions between the O - C
            if  mag(COs[i].C.pos-COs[j].O.pos) <= 2*size and dot(COs[i].C.pos-COs[j].O.pos, COs[i].C.v-COs[j].O.v) < 0: 
                COs[i].C.v, COs[j].O.v = collision(COs[i].C, COs[j].O)
            ## the collisions between the O - O
            if  mag(COs[i].O.pos-COs[j].O.pos) <= 2*size and dot(COs[i].O.pos-COs[j].O.pos, COs[i].O.v-COs[j].O.v) < 0: 
                COs[i].O.v, COs[j].O.v = collision(COs[i].O, COs[j].O)

    for CO in COs: ## change this to check and handle the collision of the atoms of all molecules on all 6 walls
        if abs(CO.O.pos.x) >= L-size and CO.O.v.x*CO.O.pos.x > 0:    
            CO.O.v.x = -CO.O.v.x
        if abs(CO.O.pos.y) >= L-size and CO.O.v.y*CO.O.pos.y > 0:    
            CO.O.v.y = -CO.O.v.y
        if abs(CO.O.pos.z) >= L-size and CO.O.v.z*CO.O.pos.z > 0:
            CO.O.v.z = -CO.O.v.z

        if abs(CO.C.pos.x) >= L-size and CO.C.v.x*CO.C.pos.x > 0:    
            CO.C.v.x = -CO.C.v.x
        if abs(CO.C.pos.y) >= L-size and CO.C.v.y*CO.C.pos.y > 0:    
            CO.C.v.y = -CO.C.v.y
        if abs(CO.C.pos.z) >= L-size and CO.C.v.z*CO.C.pos.z > 0:    
            CO.C.v.z = -CO.C.v.z

    ## sum com_K, v_K, v_P, and r_K for all molecules, respectively, to get total_com_K, total_v_K, total_v_P, total_r_K at the   
    for CO in COs:
        sum_data[0] += CO.com_K()* dt
        sum_data[1] += CO.v_K()* dt
        sum_data[2] += CO.v_P()* dt
        sum_data[3] += CO.r_K()* dt

## current moment
    times += 1
    t += dt
 
## calculate avg_com_K to be the time average of total_com_K since the beginning of the simulation, and do the same for others.    
    index = 0
    for data in sum_data:
        avg_data[index] = data/t
        index += 1

## plot avg_com_K, avg_v_K, avg_v_P, and avg_r_K
    c_avg_com_K.plot(pos = (t, avg_data[0]))
    c_avg_v_K.plot(pos = (t, avg_data[1]))
    c_avg_v_P.plot(pos = (t, avg_data[2]))
    c_avg_r_K.plot(pos = (t, avg_data[3]))