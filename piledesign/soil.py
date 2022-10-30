from dataclasses import dataclass

import numpy as np


@dataclass
class SoilProfile:
    density:float
    ground_water_depth:float = 0
    ground_water_density:float=10
    phi:float = 30
    beta:float = 0
    Nq :float = 30
    a :float = 20

    def pp_eff(self,depth:float)->float:
        return self.pp(depth)-self.u(depth)
    
    def pp(self,depth:float)->float:
        return self.density*depth

    def u(self,depth:float)->float:
        water_column = np.clip(depth-self.ground_water_depth,0,None)
        return  water_column*self.ground_water_density

    def tan_phi(self)->float:
        return np.tan(self.phi)
