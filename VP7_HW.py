from numpy import * 
from vpython import * 
 
epsilon = 8.854E-12 
N = 101         # 101*101個點
h = 1E-2/(N-1)  # 點的間距
L, d= 4E-3,1E-3 # 板長 兩板間隔
V0 = 200        # 電壓差
 
def solve_laplacian(u, u_cond, h, Niter=5000): 
    V = array(u) 
    for i in range(Niter): 
        V[u_cond] = u[u_cond] # 更新板子電位100 -100
        V[1:-1, 1:-1] = (V[:-2, 1:-1] + V[2:, 1:-1] + V[1:-1, :-2] + V[1:-1, 2:]) /4 
    return V 
 
def get_field(V, h): 
    Ex, Ey = gradient(V) 
    Ex, Ey = -Ex/h, -Ey/h 
    return Ex, Ey 
 
u = zeros([N, N]) 
u[int(N/2)-int(L/h/2.0):int(N/2)+int(L/h/2.0), int(N/2) - int(d/h/2.0)] = -V0/2 
u[int(N/2)-int(L/h/2.0):int(N/2)+int(L/h/2.0), int(N/2) + int(d/h/2.0)] = V0/2 
u_cond = not_equal(u, 0) 
### print 板子範圍 
#print(f'{int(N/2)-int(L/h/2.0)}:{int(N/2)+int(L/h/2.0)} {int(N/2) + int(d/h/2.0)}、{int(N/2) - int(d/h/2.0)}')

V = solve_laplacian(u, u_cond, h) 

scene = canvas(title='non-ideal capacitor', height=1000, width=1000, center = vec(N*h/2, N*h/2, 0)) 
scene.lights = [] 
scene.ambient=color.gray(0.99) 

# 平行板
box(pos = vec(N*h/2 , N*h/2 - d/2 - h    , 0), length = L, height = h/5, width = h) 
box(pos = vec(N*h/2 , N*h/2 + d/2 - h    , 0), length = L, height = h/5, width = h) 

# 方塊上色(表示電位)
for i in range(N): 
    for j in range(N): 
        point = box(pos=vec(i*h, j*h, 0), length = h, height= h, width = h/10, color=vec((V[i,j]+100)/200,(100-V[i,j])/200,0.0) ) 
 
Ex, Ey = get_field(V, h) 

### 箭頭(表示電場)
for i in range(0, N): 
    for j in range(0, N): 
        ar = arrow(pos = vec( i*h, j*h, h/10), axis =vec (Ex[i,j]/2E9, Ey[i,j]/2E9, 0), shaftwidth = h/6.0, color=color.black) 
###find Q, find C_nonideal = Q/(delta V) 
def capacitor(dis=1):
    flux= 0
    left, right , height = int(N/2)-int(L/h/2.0), int(N/2)+int(L/h/2.0), int(N/2) + int(d/h/2.0)
    left -= dis
    right += dis
    print(f'[non ideal]')
    print( f'Guss surface : {left}:{right} {height-dis}:{height+dis}')
    flux += sum(Ey[left:right, height +dis])*h
    flux -= sum(Ey[left:right, height -dis])*h
    flux -= sum(Ex[left-1, height-dis :height+dis+1])*h ###
    flux += sum(Ex[right, height-dis :height+dis+1])*h ###
    return flux * epsilon, flux * epsilon/V0

### Compare C_nonideal to C_ideal 
print(f'[ideal]\n C is {L*epsilon/d:.6e} F\n')
for i in range(4,5):
    Q, C = capacitor(i)
    print(f'Q is {Q:.6e} C\nC is {C:.6e} F')
    print(f'diff: {C-L*epsilon/d:.6e} F\n{(C-L*epsilon/d)/C*100:2f}%\n')

exit()
