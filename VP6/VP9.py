from vpython import*
import numpy as np
from histogram import*

# The number of atom
N = 200
# He atom are 10 times bigger for easier collision but not too big for accuracy
m, size = 4E-3/6E23, 31E-12*10
# 2L in the ccubic ontainer's original length , width, height
L = ( (24.4E-3 / (6E23)) * N) ** (1/3)/2 + size
k, T = 1.38E-23, 298.0
t, dt = 0, 3E-13
vrms = (2*k*1.5*T / m)**0.5
stage = 0       # stage number
atoms = []      # list to store atoms

### histigram setting ###
deltav = 50     #slotwidth for v histogram
vdist = graph(x=800, y=0, ymax=N*deltav/1000., width=500, height=300, xtitle='v', ytitle='dN', align='left')
theory_low_T = gcurve(color=color.red)
theory_high_T = gcurve(color=color.blue)
dv = 10.
# for the theoretical speed distribution
for v in arange(0., 4201.+dv, dv):
    theory_low_T.plot(pos=(v, (deltav/dv)*N*4.*pi * ((m/(2.*pi*k*T))**1.5) * exp((-0.5*m*v**2) / (k*T))*(v**2)*dv))
# for the simulation speed distribution
observation_0 = ghistogram(graph = vdist, bins=arange(0.,4200.,deltav), color=color.red)
observation_2 = ghistogram(graph = vdist, bins=arange(0.,4200.,deltav), color=color.blue)


### the func for handling velocity after collisions betwwen two atoms
#-----#
def vcollision(a1p, a2p, a1v,a2v):
    v1prime = a1v - (a1p - a2p) * sum((a1v-a2v)*(a1p-a2p)) / sum((a1p-a2p)**2) 
    v2prime = a2v - (a2p - a1p) * sum((a2v-a1v)*(a2p-a1p)) / sum((a2p-a1p)**2) 
    return v1prime, v2prime

### adiabatic compresssion ###
def compression(container):
    global stage
    if container.length > L:
        container.length -= L/10000
    elif container.length <= L:
        stage +=1
    if stage == 2:
        T = sum(E_k) / (3*N*k/2)
        for v in arange(0., 4201.+dv, dv):
            theory_high_T.plot(pos=(v, (deltav/dv)*N*4.*pi * ((m/(2.*pi*k*T))**1.5) * exp((-0.5*m*v**2) / (k*T))*(v**2)*dv))


### keyboard ###
def keyinput(evt):
    global stage, T, container
    keyboard = evt.key
    if keyboard == 'n':
        stage += 1
    """
    stage 0 --- origin
    stage 1 --- process of compression and freeze graph1
    stage 2 --- stop compression and new graph
    stage 3 ---  free expansion
   """
    # plot the theory velocity distubution curve
    if stage == 2:
        T = sum(E_k) / (3*N*k/2)
        for v in arange(0., 4201.+dv, dv):
            theory_high_T.plot(pos=(v, (deltav/dv)*N*4.*pi * ((m/(2.*pi*k*T))**1.5) * exp((-0.5*m*v**2) / (k*T))*(v**2)*dv))
    # volume recover to origin
    if stage == 3:
        container.length = 2*L
### output ###
# T,  p,  V,  p*V,  N*k*T,  p*(V**gamma)
def data_output(container, momentum, kenetic_total):
    global N, k, dt, t
    gamma_ideal = 5/3
    
    # 3/2*N*k*temp = kenetic energy
    temp = kenetic_total / (3*N*k/2)
    # force = momentum / passed time
    # pressure = force / area of 6 walls
    wall_area = 2*(container.length * container.height + container.height * container.width + container.width * container.length)
    p = sum(momentum) / t / wall_area#(momentum[0]**2 + momentum[1]**2 + momentum[2]**2) **0.5 / t / wall_area
    # volume
    V = container.length * container.height * container.width
    
    print(f'T={temp:.2f}, p={p:.2E}, V={V:.2E}, p*V={p*V:.2E}, N*k*T={N*k*temp:.2E}, p*(V**gamma)={p*(V**gamma_ideal):.2E}')


### initialization ###
scene = canvas(width=500, height=500, background=vector(0.2,0.2,0), align = 'left') 
scene.bind("keydown", keyinput)
container = box(length = 2*L, height = 2*L, width = 2*L,    opacity=0.2, color = color.yellow ) 
# particle position array and particle velocity array, N particles and 3 for x,y,z
p_a, v_a = np.zeros((N,3)), np.zeros((N,3))
for i in range(N):
    # partiale is at random position
    p_a[i] = [2 * L*random() - L, 2 * L*random() - L, 2 * L*random() - L]  # particle is initially random positioned in container 
    if i ==N-1:
        atom = sphere(pos=vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]), radius = size, color=color.yellow, make_trail = True, retain = 50) 
    else:
        atom = sphere(pos=vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]), radius = size, color=vector(random(), random(), random()))
    ra = pi* random()
    rb = 2*pi*random()
    # atoms get equal velocity but different angle
    v_a[i] = [vrms*sin(ra)*cos(rb), vrms*sin(ra)*sin(rb), vrms*cos(ra)]
    atoms.append(atom)
#-------------------------------------------------------------------------------
momentum_change = [0, 0, 0]
while True:
    t += dt
    rate(10000)
    # caculate new position for all atoms
    p_a += v_a*dt
    # to display atoms at new positions
    for i in range(N): atoms[i].pos = vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]) 
    
    ### stage change ###
    # plot velocity distrbution at low temp
    if stage == 0 : observation_0.plot(data = np.sqrt(np.sum(np.square(v_a),-1)))
    # volume change
    if stage == 1 : compression(container)
    # plot velocity distrbution at high temp
    if stage == 2 or stage == 3 : observation_2.plot(data = np.sqrt(np.sum(np.square(v_a),-1)))


    ### find collision between pairs of atoms, and handle their collisions
    #-----#
    r_array = p_a - p_a[:, np.newaxis]                      # array for vector from one atom to another atom for all pairs of atoms
    rmag = np.sqrt(np.sum(np.square(r_array), -1))          # distance array between atoms for all pairs of atoms 
    hit = np.less_equal(rmag, 2*size) - np.identity(N)      # if smaller than 2*size meaning these two atoms might hit each other
    hitlist = np.sort(np.nonzero(hit.flat)[0]).tolist()     # change hit to a list  
    for ij in hitlist:                                      # i,j encoded as i*N atoms+j  
        i, j = divmod(ij,N)                                # atom pair, i-th and j-th atoms, hit each other
        hitlist.remove(j*N+i)                              # remove j,i pair from list to avoid handling the collision twice 
        if sum((p_a[i]-p_a[j])*(v_a[i]-v_a[j])) < 0 :       # only handling collision if two atoms are approaching each other
            v_a[i], v_a[j] = vcollision(p_a[i], p_a[j], v_a[i], v_a[j]) # handle collision    
    """
    some description of funtion
    p_a[:, np.newaxis] --> 2D array to 3D array
    """
    #find collisions between the atoms and the walls, and handle their elastic collisions 
    for i in range(N): 
        if abs(p_a[i][0]) >= container.length/2 - size and p_a[i][0]*v_a[i][0] > 0 : 
            if stage == 1:
                if v_a[i][0] > 0:
                    v_a[i][0] = - v_a[i][0] - 2*L/20000/dt
                elif v_a[i][0] < 0:
                    v_a[i][0] = - v_a[i][0] + 2*L/20000/dt
                momentum_change[0] += 2*m*abs(v_a[i][0]) + 2*m*L/20000/dt
            else:
                v_a[i][0] = - v_a[i][0]
                momentum_change[0] += 2*m*abs(v_a[i][0])
        if abs(p_a[i][1]) >= L - size and p_a[i][1]*v_a[i][1] > 0 : 
            v_a[i][1] = - v_a[i][1]
            momentum_change[1] += 2*m*abs(v_a[i][1])
        if abs(p_a[i][2]) >= L - size and p_a[i][2]*v_a[i][2] > 0 : 
            v_a[i][2] = - v_a[i][2]
            momentum_change[2] += 2*m*abs(v_a[i][2])
    
    ### output ###
    if t >= 1000*dt:
        v_2 = np.sum(np.square(v_a),-1)     # square of velocity of atoms
        E_k = 1/2 * m * v_2                 # kenetic energy of each atom
        data_output(container, momentum_change, sum(E_k))   # print data
        t = 0
        momentum_change = [0, 0, 0]