from vpython import*

G = 6.673E-11
mass = {'sun':1.989E60, 'earth':5.972E24, 'mars':6.4169E23, 'halley':2.2E14 }
d_at_perihelion = {'earth':1.495E11, 'mars':2.279E11, 'halley': 8.7665E10}
v_at_perihelion = {'earth': 2.9783E4, 'mars':2.4077E4, 'halley': 54563.3}

# the force sun give
def G_force(m, pos_vec):
    return -G * m * mass['sun'] / mag2(pos_vec) * norm(pos_vec)

# planet object
def G_force(m, pos_vec): 
    return -G * mass['sun'] * m / mag2(pos_vec) * norm(pos_vec) 
 
class as_obj(sphere): 
    def kinetic_energy(self): 
        return 0.5 * self.m * mag2(self.v) 
    def potential_energy(self): 
        return - G * mass['sun'] * self.m / mag(self.pos) 
 
scene = canvas(width=800, height=800, background=vector(0.5,0.5,0)) 
scene.lights = [] 
sun = sphere(pos=vector(0,0,0), radius = 3.0E10, color = color.orange, emissive=True) 
local_light(pos=vector(0,0,0)) 
earth = as_obj(pos = vector(d_at_perihelion['earth'],0,0), radius = 1.5E10, m = mass['earth'], texture={'file':textures.earth}, make_trail = True) 
earth.v = vector(0, 0, - v_at_perihelion['earth']) 
mars = as_obj(pos = vector(d_at_perihelion['mar
us'],0,0), radius = 1.0E10, m = mass['mars'], color = color.red, make_trail = True) 
mars.v = vector(0, 0, - v_at_perihelion['mars']) 
#halley = as_obj(pos = vector(d_at_perihelion['halley'],0,0), radius = 0.5E10, m = mass['halley'], make_trail = True) 
#halley.v = vector(0, 0, - v_at_perihelion['halley']) 
 
stars = [earth, mars] 
dt=60*60*6 
print(earth.potential_energy(), earth.kinetic_energy()) 
 
while True: 
    rate(1000) 
    for star in stars: 
        star.a = G_force(star.m, star.pos) / star.m 
        star.v = star.v + star.a * dt 
        star.pos = star.pos + star.v * dt 