from vpython import*

class planet(sphere):
    pos0 = vector(0,0,0)
    pos1 = vector(0,0,0)
    v = vector(0,0,0)
    m = 0
    def second_law(self, star_pos, dt):        # other pos of stars
        a1 = self.pos1 - star_pos
        a0 = self.pos0 - star_pos
        area = (mag2(a1)*mag2(a0) - (dot(a1, a0))**2)**0.5
        return area / dt