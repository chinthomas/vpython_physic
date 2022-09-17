from vpython import*

size, m_o, m_c, k_bond = 31E-12, 16.0/6E23, 12.0/6E23, 18600.0
d = 2.5*size
dt = 1E-16

class CO_molecule:
    def __init__(self, pos, axis):
        self.O = sphere(pos = pos, radius = size, color = color.red)
        self.C = sphere(pos = pos + axis, radius = size, color = color.blue)
        self.bond = cylinder(pos = pos, axis = axis, radius = size/2.0, color = color.white)
        self.O.m = m_o
        self.C.m = m_c
        self.O.v = vector(0, 0, 0)
        self.C.v = vector(0, 0, 0)
        self.bond.k = k_bond        ### k_bond is ...

    def bound_force_on_O(self):     # retrun bound force acted on O atom
        return self.bond.k*(mag(self.bond.axis) - d)* norm(self.bond.axis)

    def time_lapse(self, dt):       # caculate a, v, pos, axis of atom
        self.C.a = -self.bound_force_on_O()/self.C.m
        self.O.a = self.bound_force_on_O()/self.O.m
        self.C.v += self.C.a * dt
        self.O.v += self.O.a * dt
        self.C.pos += self.C.v* dt
        self.O.pos += self.O.v* dt
        self.bond.axis = self.C.pos - self.O.pos
        self.bond.pos = self.O.pos

    def com(self):                  # return the position of center of mass  
        return (self.C.pos*self.C.m + self.O.pos*self.O.m)/(self.C.m + self.O.m)
    def com_v(self):                # return velocity of center of mass
        return (self.C.v*self.C.m + self.O.v*self.O.m)/(self.C.m + self.O.m)   
    def v_P(self):        # return potential energy of the bond for the vibration motion 
        return self.bond.k * (mag(self.bond.axis)-d)**2/2.0 
    def v_K(self):        # return kinetic energy of the vibration motion 
        return (self.O.m* dot(self.O.v - self.com_v(), (self.bond.axis)/mag(self.bond.axis))**2 + self.C.m* (dot(self.C.v - self.com_v(), self.bond.axis)/mag(self.bond.axis))**2 ) /2 
    def r_K(self):        # return kinetic energy of the rotational motion   
        return (self.O.m* mag(cross(self.O.v - self.com_v(), (self.bond.axis))/mag(self.bond.axis))**2 + self.C.m* (mag(cross(self.C.v - self.com_v(), self.bond.axis))/mag(self.bond.axis))**2 ) /2
    def com_K(self):        #return kinetic energy of the translational motion of the center of mass 
        return (self.C.m+self.O.m)*mag2(self.com_v())/2 
    
def collision(a1, a2):
    v1prime = a1.v - 2*a2.m/(a1.m+a2.m) *(a1.pos-a2.pos) * dot (a1.v-a2.v, a1.pos-a2.pos) / mag(a1.pos-a2.pos)**2 
    v2prime = a2.v - 2*a1.m/(a1.m+a2.m) *(a2.pos-a1.pos) * dot (a2.v-a1.v, a2.pos-a1.pos) / mag(a2.pos-a1.pos)**2
    return v1prime, v2prime

def equal(a, b):
    if isinstance(a, vector):
        return equal(a.x, b.x) and equal(a.y, b.y) and equal(a.z, b.z)
    if isinstance(a, float):
        return abs(a-b) < 1E-25
    
if __name__ == '__main__':
    a = CO_molecule(pos = vector(0, 0, 0), axis = vector(2.6*size, 0, 0))
    a.O.v = vector(1.0, 1.0, 0)
    a.C.v = vector(2.0, -1.0, 0)
    a.time_lapse(dt)
    print('bound force acted on O    : ', equal(a.bound_force_on_O(), vector(5.76609e-08, -1.43079e-13, 0)), a.bound_force_on_O(), '# (5.76609e-08, -1.43079e-13, 0)')
    print('pos of center of mass     : ', equal(a.com(), vector(3.4543e-11, 1.42857e-17, 0)), a.com(), '# (3.4543e-11,  1.42857e-17,  0)')
    print('velocity of center of mass: ', equal(a.com_v(), vector(1.42857, 0.142857, 0)), a.com_v(), '# (1.42857, 0.142857, 0)')
    print('P of bond of vib.motion   : ', equal(a.v_P(), 8.937585694598954e-20), a.v_P(), '# 8.937585694598954e-20')
    print('K of vib.motion           : ', equal(a.v_K(), 1.4028593914919891e-24), a.v_K(), '# 1.4028593914919891e-24')
    print('K of rot.motion           : ', equal(a.r_K(), 2.2857114754936572e-23),a.r_K(), '# 2.2857114754936572e-23')
    print('K of trans.motion of com  : ', equal(a.com_K(), 4.8095238095238086e-23), a.com_K(), '# 4.8095238095238086e-23')
    