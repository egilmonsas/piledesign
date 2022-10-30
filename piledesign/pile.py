from dataclasses import dataclass

import numpy as np
import scipy as sp

from piledesign.soil import SoilProfile


@dataclass
class Pile:
    _PI = 3.14159265359
    def __init__(self,diameter:float,length:float):
        """
        Parameters
        ----------
        diameter : float
            Diameter of pile section [m]
            
        length : float
            Length of pile [m]
        """
        self.diameter=diameter
        self.length=length
        self.shear_ratio=0.3
    def utilization(self,N,soil:SoilProfile)->float:
        return N/self.bearing_capacity(soil)

    def bearing_capacity(self,soil:SoilProfile)->float:
        return self.shaft_friction(soil) + self.tip_resistance(soil)

    def shaft_friction(self,soil)->float:
        tau = lambda z: (soil.pp_eff(z)+soil.a)
        return self.shear_ratio*_simpson(tau,0,self.length,10)*self.perimeter()

    def tip_resistance(self,soil):
        sigma_pm = (soil.Nq-1)*(soil.pp_eff(self.length)+soil.a)
        return self.area()*sigma_pm

    def area(self)->float:
        return self._PI/4 * self.diameter**2 

    def perimeter(self)->float:
        return self._PI * self.diameter

# Some bug in scipy/numpy means we need an explicit integral function
def _simpson(f,a,b,N_half=10):
    h=(b-a)/(2*N_half)
    res = f(a) + f(b) + 4*np.sum([f(2*j-1) for j in range(1,N_half)])+ 2*np.sum([f(2*j) for j in range(1,N_half-1)])
    return (h/3)*res
