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

    def bearing_capacity(self,soil:SoilProfile)->float:
        return self.shaft_friction(soil) + self.tip_resistance(soil)

    def shaft_friction(self,soil)->float:
        const=self.perimeter()*self.shear_ratio
        return(const*sp.integrate.quad(lambda z: soil.pp(z),0,10)[0])


    def tip_resistance(self,soil):
        sigma_pm = (soil.Nq-1)*(soil.pp_eff(self.length)+soil.a)
        return self.area()*sigma_pm

    def area(self)->float:
        return self._PI/4 * self.diameter**2 

    def perimeter(self)->float:
        return self._PI * self.diameter
