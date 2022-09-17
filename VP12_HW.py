from ctypes import sizeof
from vpython import * 
from numpy import * 
 
N = 100 
R, lamda = 1.0, 500E-9 
d = 100E-6 
 
dx, dy = d/N, d/N 
scene1 = canvas(align = 'left', height=600, width=600, center = vector(N*dx/2, N*dy/2, 0)) 
scene2 = canvas(align = 'right', x=600, height=600, width=600, center = vector(N*dx/2, N*dy/2, 0)) 
scene1.lights, scene2.lights = [], [] 
scene1.ambient, scene2.ambient = color.gray(0.99), color.gray(0.99) 
side = linspace(-0.01*pi, 0.01*pi, N) 
x,y = meshgrid(side,side) # coordination of grid of aperture

# change this to calculate the electric field of diffraction of the aperture  
E_field = zeros((100,100))

k_x = 2*pi/lamda*x/R # wavelength *theta /R
k_y = 2*pi/lamda*y/R # wavelength *theta /R
"""
for screen_x in range(-N//2,N//2+1):
    for screen_y in range(-N//2,N//2+1):
        if (screen_x**2 + screen_y**2) <= (d/2)**2:
            E_field += cos(k_x*screen_x+k_y*screen_y)/R*dx*dy    
"""
for i in linspace(-d,d,100):
    for j in linspace(-d,d,100):
        if (i**2 + j**2) <= (d/2)**2:
            E_field += cos(k_x*i+k_y*j)/R*dx*dy

Inte = abs(E_field) ** 2 
maxI = amax(Inte) 
for i in range(N): 
    for j in range(N): 
        box(canvas = scene1, pos=vector(i*dx, j*dy, 0), length = dx, height= dy, width = dx,  
  color=vector(Inte[i,j]/maxI,Inte[i,j]/maxI,Inte[i,j]/maxI)) 

# print first dark
I_min = Inte[N//2, N//2] # minimun of light intensity
theta = 0                # total turned angle
for r in range(N//2, N):
    if Inte[r,r] < I_min:
        I_min = Inte[r,r]
        theta += 0.01*2*pi/N  # 每隔大小(rad)
    elif Inte[r,r] > I_min :
        break
        
print(f'exp.  result  of  theata : {theta * 2}')

Inte = abs(E_field) 
maxI = amax(Inte) 
for i in range(N): 
    for j in range(N): 
        box(canvas = scene2, pos=vector(i*dx, j*dy, 0), length = dx, height= dy, width = dx,  
            color=vector(Inte[i,j]/maxI,Inte[i,j]/maxI,Inte[i,j]/maxI))

print(f'theorical value of theta : {1.22*lamda/d}')