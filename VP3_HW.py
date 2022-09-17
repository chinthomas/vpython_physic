###### moom orbit precession #######

from vpython import*

mass = {'earth': 5.97E24, 'moon': 7.36E22, 'sun':1.99E30} 
radius = {'earth': 6.371E6*10, 'moon': 1.317E6*10, 'sun':6.95E8*10}     #10 times larger for better view  
earth_orbit = {'r': 1.495E11, 'v': 2.9783E4} 
moon_orbit = {'r': 3.84E8, 'v': 1.022E3} 
theta = 5.145*pi/180.0  
G = 6.673E-11

### 背景設定 & 星球設定
scene = canvas(width = 800, height = 800, background = vec(0.1,0.1,0.1))

moon = sphere(pos = vector(moon_orbit['r']*mass['earth']/(mass['earth'] + mass['moon']), 0, 0), radius = radius['moon'], m = mass['moon'], make_trail = True)
moon.v = vector(0, 0, -moon_orbit['v'])
earth = sphere(pos = vector(-1*moon_orbit['r']*mass['moon']/(mass['earth'] + mass['moon']), 0, 0), radius = radius['earth'], m = mass['earth'], texture = {'file':textures.earth})
earth.v = vector(0, 0, 0)

# 重力公式: 1 受力物 2 施力物
def G_force(m1, m2, pos1, pos2):
    return -G * m1 * m2 / mag2(pos1 - pos2) * norm(pos1 - pos2)

# 質心速度為零
earth.v = vector(0, 0, moon_orbit['v'] * mass['moon'] / mass['earth']) 

# 月球軌道傾斜
#distance = (moon.pos - earth.pos)
#moon.pos = earth.pos + vector(distance.x * cos(theta), - distance.x * sin(theta), 0)

###############################################################
dt = 60*60
while True:
    rate(1000)

    moon.a = G_force(mass['moon'], mass['earth'], moon.pos, earth.pos) / mass['moon']
    earth.a = G_force(mass['earth'], mass['moon'], earth.pos, moon.pos) / mass['earth']
    moon.v += moon.a * dt
    moon.pos += moon.v * dt
    earth.v += earth.a * dt
    earth.pos += earth.v * dt
    #scene.center = earth.pos
