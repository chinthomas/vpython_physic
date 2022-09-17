from vpython import* 
 
fd = 120                 # 120Hz 
#(Your Parameters here) 
R = 30 
C = 2E-5
L = 2E-1
t = 0 
dt = 1.0/(fd * 5000)     # 5000 simulation points per cycle 
### theorem value
Z = (R**2 + (-1/C/(2*pi*fd) + L*2*pi*fd)**2 )**(1/2)
phase_theorem = atan((-1/C/(2*pi*fd) + L*2*pi*fd)/R)

### scene of graph
scene1 = graph(align = 'left', xtitle='t', ytitle='i (A) blue, v (100V) red,', background=vector(0.2, 0.6, 0.2)) 
scene2 = graph(align = 'left', xtitle='t', ytitle='Energy (J)', background=vector(0.2, 0.6, 0.2)) 
 
i_t = gcurve(color=color.blue, graph = scene1) 
v_t = gcurve(color=color.red, graph = scene1) 
E_t = gcurve(color=color.red, graph = scene2) 

### t < 0
i = 0
v = 0
v_c = 0
i_L = 0
###
i_mag = 0
v_mag = 0
E_mag = 0
println = False
while t < 20*(1/fd):
    rate(5000)

    ### 電壓源變化
    if t < 12*(1/fd) and t > 0: v = 36 * sin(2*pi*fd*t)
    else: v = 0
    
    ### 被動變化    
    v_L = v - v_c - i*R
    i_c = i
    i = i_L
    ### 主動變化
    i_L += v_L / L * dt
    v_c += i_c / C * dt
    
    ### 能量變化
    E = C*v_c**2/2 + L*i_L**2/2
    ### 作圖
    i_t.plot(pos = (t, i))
    v_t.plot(pos = (t, v/100))
    E_t.plot(pos = (t, E))
    
    ### current magnitude and phase
    if t < (10/fd) and t > (9/fd):
        if i_mag < i:
            i_mag = i
            t_i_mag = t
        if v_mag < v:
            v_mag = v
            t_v_mag = t
        if E_mag < E:
            E_mag = E
    elif t > (10/fd) and not println :
        print('(2)')
        print(f'stimulated Im: {i_mag:.6f}A')
        print(f'theorem    Im: {36/Z:.6f}A')
        println = True
        phase = ((t_i_mag-t_v_mag)%(1/fd)) / (1/fd) * 360
        x = 'lags'
        if t_i_mag < t_v_mag:x='leads'
        print(f'current {x} voltage {phase:.6f}deg')
        print(f'theorem: {phase_theorem/pi*180:.6f}deg')
        print('')    
    ### energy decay
    if t > (12/fd) and E < E_mag/10 and E_mag!=0:
        print('(3)')
        print(f'energy decay at time {t:.6f}s, {t*fd:.6f}T')
        print(f'which is {t-(12/fd):.6f}s after voltage turned off')
        E_mag = 0
    t += dt