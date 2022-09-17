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

moon = sphere(pos = vector(moon_orbit['r'], 0, 0), radius = radius['moon'])
moon.v = vector(0, 0, -moon_orbit['v'])
earth = sphere(pos = vector(0, 0, 0), radius = radius['earth'], texture = {'file':textures.earth})
earth.v = vector(0, 0, 0)
sun = sphere(pos =vector(0, 0, 0), radius = radius['sun'], color = color.orange, emissive = True)
scene.lights = []
local_light(pos = sun.pos)

# 重力公式: 1 受力物 2 施力物
def G_force(m1, m2, pos1, pos2):
    return -G * m1 * m2 / mag2(pos1 - pos2) * norm(pos1 - pos2)

# 質心速度為零
vcm = (earth.v * mass['earth'] + moon.v * mass['moon']) / (mass['earth'] + mass['moon'])
earth.v = earth.v - vector(0, 0, earth_orbit['v']) - vcm
moon.v = moon.v - vector(0, 0, earth_orbit['v']) - vcm

# 質心位置在中央
xcm = (earth.pos * mass['earth'] + moon.pos * mass['moon']) / (mass['earth'] + mass['moon'])
earth.pos = earth.pos - vector(0, 0, earth_orbit['r']) - xcm
moon.pos = moon.pos - vector(0, 0, earth_orbit['r']) - xcm

# 月球軌道傾斜
moon.pos = vector(moon.pos.x * cos(theta), -moon.pos.x * sin(theta), 0) 

###############################################################
dt = 60*60*6
while True:
    rate(100)

    moon.a = (G_force(mass['moon'], mass['earth'], moon.pos, earth.pos) + G_force(mass['moon'], mass['sun'], moon.pos, sun.pos)) / mass['moon']
    moon.v += moon.a * dt
    moon.pos += moon.v * dt

    earth.a = (G_force(mass['earth'], mass['moon'], earth.pos, moon.pos) + G_force(mass['earth'], mass['sun'], earth.pos, sun.pos)) / mass['earth']
    earth.v += earth.a * dt
    earth.pos += earth.v * dt
    scene.center = earth.pos
