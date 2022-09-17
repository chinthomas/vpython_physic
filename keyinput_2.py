from typing_extensions import ParamSpecArgs
from vpython import*
pos, angle = vector(0, 0, 0), 0

def right(b):
    global pos, angle
    pos = pos + vector(0.1, 0, 0)

def left(b):
    global pos, angle
    pos = pos + vector(-0.1, 0, 0)

scene = canvas(width = 400, height=400, range=5, background=color.white)
ball = sphere(radius = 2, texture = textures.earth)

# create button on screen
button(text="left", pos=scene.title_anchor, bind = left)
button(text="right", pos=scene.title_anchor, bind = right)

while True: 
        rate(1000) 
        ball.rotate(angle=pi/600, axis= vector(sin(angle),cos(angle),0), origin=pos) 
        ball.pos = pos 
