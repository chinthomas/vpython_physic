from vpython import*

mass = {'earth': 5.97E24, 'moon': 7.36E22, 'sun':1.99E30} 
radius = {'earth': 6.371E6*10, 'moon': 1.317E6*10, 'sun':6.95E8*10}     #10 times larger for better view  
earth_orbit = {'r': 1.495E11, 'v': 2.9783E4} 
moon_orbit = {'r': 3.84E8, 'v': 1.022E3} 
theta = 5.145*pi/180.0  
G = 6.673E-11
# 重力公式: 1 受力物 2 施力物
def G_force(obj1, obj2):
    return -G * obj1.m * obj2.m / mag2(obj1.pos - obj2.pos) * norm(obj1.pos - obj2.pos)

# 進動在XZ平面跟軸的夾角
def angle_xz(vec):
    return acos(vec.x * 1 / 1 / mag(vec))

### 背景設定
scene = canvas(width = 800, height = 800, background = vec(0.1,0.1,0.1))

### 地月系統設定

moon = sphere(pos = vector(moon_orbit['r'], 0, 0), radius = radius['moon'], m = mass['moon'],make_trail = True)
moon.v = vector(0, 0, -moon_orbit['v'])
earth = sphere(pos = vector(0, 0, 0), radius = radius['earth'], m = mass['earth'], texture = {'file':textures.earth})
earth.v = vector(0,0,0)

# 月球軌道傾斜
distance = (moon.pos - earth.pos)
moon.pos = earth.pos + vector(distance.x * cos(theta), - distance.x * sin(theta), 0)


# 地月系統動量守恆
xcm = (earth.pos*earth.m + moon.pos*moon.m) /(earth.m + moon.m)
earth.pos -= xcm
moon.pos -= xcm
vcm = (earth.v*earth.m + moon.v*moon.m) /(earth.m + moon.m)
earth.v -= vcm
moon.v -= vcm

# 在太陽軌道上的位置和初速
earth.pos += vector(earth_orbit['r'], 0, 0)
moon.pos += vector(earth_orbit['r'], 0, 0)

earth.v -= vector(0, 0, earth_orbit['v'])
moon.v -= vector(0, 0, earth_orbit['v'])


### 設定太陽
sun = sphere(pos =vector(0, 0, 0), radius = radius['sun'], color = color.orange, m = mass['sun'], emissive = True)
scene.lights = []
local_light(pos = sun.pos)

# 設定地月軌道面方向箭頭
L = arrow()
L.pos = earth.pos
L.axis = norm(cross((earth.pos - moon.pos), (earth.v - moon.v)))*radius['earth']*3
begin = angle_xz(L.axis)

###############################################################
dt = 60*60*6
t =0
while True:
    rate(1000)
    t += 1/365/4 # t表示經過幾年
    moon.a = (G_force(moon, earth)) / mass['moon']
    moon.v += moon.a * dt
    moon.pos += moon.v * dt

    earth.a = (G_force(earth, moon)) / mass['earth']
    earth.v += earth.a * dt
    earth.pos += earth.v * dt
    #scene.center = earth.pos

    L.pos = earth.pos
    L.axis = norm(cross((earth.pos - moon.pos), (earth.v - moon.v)))*radius['earth']*3
    if abs(angle_xz(L.axis) - begin) <0.00001 and t > 0.8:
        print(f'The moon precession is {t} years')

