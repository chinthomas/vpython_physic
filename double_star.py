from vpython import*
# mass kg
m1 = 2
m2 = 2
G = 6.673E-11

scene = canvas(width = 800, height = 800, background = vec(0.9, 0.9, 0.9))

star1 = sphere(pos = vector(r *m2 /(m1 +m2), 0, 0), radius = 5, m = m1, color = color.blue, make_trail = True)
star2 = sphere(pos = vector(r *m1 /(m1 +m2), 0, 0), radius = 5, m = m2, color = color.red, make_trail = True)

### 
def G_f(obj1, obj2):
    return -G * obj1.m * obj2.m / mag2(obj1.pos - obj2.pos) * norm(obj1.pos - obj2.pos)

while True:
    star1.a = G_f(star1,star2) / star1.m
    star2.a = G_f(star2,star1) / star2.m

    star1.v = star1.a * dt
    star2.v = star2.a * dt

    star1.pos = star1.v * dt
    star2.pos = star2.v * dt