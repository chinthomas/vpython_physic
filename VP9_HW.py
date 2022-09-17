import numpy as np
from vpython import*

N = 500
u0 = 4*np.pi*1E-7

# scene = canvas(width=600, height=600,align = 'left', background=vector(0.2,0.2,0)) 

def Biot_Savart(pos1:vector, pos2:vector,current,ds:vector) -> vector:
    r = pos2-pos1
    return u0/4/np.pi*current*ds.cross(r.norm())/mag(r)**2

class ring:
    def __init__(self, r, z, n, current=0) -> None:
        self.theta = np.linspace(0, 2*np.pi, n)
        self.n, self.r = n, r
        self.z = z
        self.pos = [ vector(r*np.cos(self.theta[i]), r*np.sin(self.theta[i]), z) for i in range(n)]
        self.ds = [ (2*np.pi*r/n)*vector( -np.sin(self.theta[i]), np.cos(self.theta[i]), 0) for i in range(n)]
        self.current = current

    def draw(self):
        self.obj = []
        for i in range(self.n):
            self.obj.append(sphere(pos=self.pos[i], radius=0.1))
    
    def B_at_P(self, pos) -> vector:
        """ ring在點P產生的磁場 """
        B = vector(0,0,0)
        for pos_ring, ds in zip(self.pos, self.ds):
            B += Biot_Savart(pos_ring, pos, self.current, ds)
        return B
    
def find_Mutual_indutance(ring_A:ring, ring_B:ring):
    # ring_A 有電流
    # ring_B 沒電流
    ring_A.current = 1
    ring_B.current = 0

    # 分割面積
    dr = ring_B.r/ring_B.n
    flux = 0
    for r in np.linspace(0,ring_B.r, ring_B.n+1):
        P = vector(r,0,ring_B.z)   # P 位置
        A = 2*np.pi*r*dr
        B = ring_A.B_at_P(P)
        flux += dot(B,vector(0,0,A))
    return flux/ring_A.current


ring1 = ring(r=0.16, z=0, n=N)
ring2 = ring(r=0.06, z=0.10, n=N)
m21 = find_Mutual_indutance(ring1,ring2)
m12 = find_Mutual_indutance(ring2,ring1)
print(f'M21:{m21}H\nM12:{m12}H')