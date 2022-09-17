from vpython import*

pos, angle = vector(0, 0, 0), 0

# keyboard callback function
def keyinput(evt):
    global pos, angle
    move = {
        "left": vector(-0.1, 0, 0), 
        "right": vector(0.1, 0, 0),
        "up": vector(0, 0.1, 0),
        "down": vector(0, -0.1, 0),
        'i': vector(0, 0, -0.1),
        'o': vector(0, 0, 0.1)
    }
    roa = {'c':pi/90.0, 'r': -pi/90.0}
    # get the key that press down
    s = evt.key
    if s in move: pos = pos + move[s]
    if s in roa:
        ball.rotate(angle = roa[s], axis = vector(0, 0, 1), origin = ball.pos)
        angle = angle - roa[s]

scene = canvas(width=800, height=800, range=5, background=color.white)
ball = sphere(radius=3.0, texture = textures.earth)
# bind func. keyinput with scene
# when the event "keydown" happen, execute keyinput()
scene.bind("keydown", keyinput)

while True:
    rate(1000)
    ball.rotate(angle=pi/600, axis=vector(sin(angle), cos(angle), 0), origin = pos)
    ball.pos = pos