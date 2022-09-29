import numpy as np
from collections.abc import Iterable
from matplotlib import pyplot as plt

def to_array(x,dim=2):
    if isinstance(x,Iterable):
        return np.array(x)
    else:
        return np.array((x,)*dim)

class Stat:
    def __init__(self, x=0, angle=0, v=0, rv=0):
        self.x=to_array(x, 2)
        self.angle=to_array(angle, 1)
        self.v=to_array(v, 2)
        self.rv=to_array(rv, 1)

    def __repr__(self):
        return str(self.to_array())

    def to_array(self):
        return np.concatenate([self.x, self.angle, self.v, self.rv])

    def move(self, iters=1, t=1, a=0,ra=0):
        p=[np.concatenate([self.x, self.angle])]
        s=self.to_array()
        A=np.array([[1, 0, 0, t, 0, 0, .5*t**2, 0, 0],
                    [0, 1, 0, 0, t, 0, 0, .5*t**2, 0],
                    [0, 0, 1, 0, 0, t, 0, 0, .5*t**2],
                    [0, 0, 0, 1, 0, 0, t, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, t, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, t]])
        for i in range(iters):
            if type(a) is np.ndarray and len(a.shape)==2:
                x=np.concatenate([s, a[i], ra[i]])
            else:
                a=to_array(a, 2)
                ra=to_array(ra, 1)
                x=np.concatenate([s, a, ra])

            s=np.dot(A,x)
            p.append(s[:3])

        return Stat(s[:2], s[2], s[3:5], s[5]), np.array(p)
