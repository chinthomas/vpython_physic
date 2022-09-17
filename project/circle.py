from vpython import*

G = 6.673E-11
mass = {'sun':1.989E60, 'earth':5.972E24, 'mars':6.4169E23, 'halley':2.2E14 }
d_at_perihelion = {'earth':1.495E11, 'mars':2.279E11, 'halley': 8.7665E10}
v_at_perihelion = {'earth': 2.9783E4, 'mars':2.4077E4, 'halley': 54563.3}
def G_force(m, pos_vec):
    return -G * m * mass['sun'] / mag2(pos_vec) * norm(pos_vec)
scene = canvas(width=800, height=800, background=vector(0.5, 0.5, 0))
sun = sphere(pos = vector(0, 0, 0), radius = 3E12)
earth = sphere(pos = vector(d_at_perihelion['earth'],0 ,0), radius=1.5E10, m=mass['earth'], texture={'file':textures.earth}, make_trail=True)
earth.v = vector(0, 0, -v_at_perihelion['earth'])
stars = [earth]
dt=60*60*6
scene.forward = vector(0, -1, 0)
while True:
    rate(100)
    for star in stars:
        star.a = G_force(star.m, star.pos) / star.m
        star.v = star.v + star.a * dt
        star.pos = star.pos +star.v * dt