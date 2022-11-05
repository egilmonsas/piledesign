from dataclasses import dataclass

import numpy as np

from piledesign.gis import Coordinate
from piledesign.material import Material
from piledesign.soil import SoilProfile


@dataclass
class Pile:
    _PI = 3.14159265359

    def __init__(
        self,
        pos: Coordinate,
        diameter: float,
        length: float,
    ):
        """
        Parameters
        ----------
        diameter : float
            Diameter of pile section [m]

        length : float
            Length of pile [m]
        """
        self.pos = pos
        self.diameter = diameter
        self.length = length
        self.shear_ratio = 0.3
        self.material = Material(500, 7, 9)

    def utilization(self, N, soil: SoilProfile, f_tot: float = 1.0) -> float:
        return N / self.bearing_capacity(soil, f_tot)

    def section_capacity(self) -> float:
        return np.clip(self.area() * self.material.f_compressive * 1000, 0.01, None)

    def section_utilization(self, N) -> float:
        return N / self.section_capacity()

    def bearing_capacity(self, soil: SoilProfile, f_tot: float = 1.0) -> float:
        return (self.shaft_friction(soil) + self.tip_resistance(soil)) / f_tot

    def shaft_friction(self, soil) -> float:
        tau = lambda z: (soil.pp_eff(z) + soil.a)
        return self.shear_ratio * _simpson(tau, 0, self.length, 10) * self.perimeter()

    def tip_resistance(self, soil):
        sigma_pm = (soil.Nq - 1) * (soil.pp_eff(self.length) + soil.a)
        return self.area() * sigma_pm

    def area(self) -> float:
        return self._PI / 4 * self.diameter**2

    def perimeter(self) -> float:
        return self._PI * self.diameter


# Some bug in scipy/numpy means we need an explicit integral function
def _simpson(f, a, b, N_half=10):
    h = (b - a) / (2 * N_half)
    res = (
        f(a)
        + f(b)
        + 4 * np.sum([f(2 * j - 1) for j in range(1, N_half)])  # type ignore
        + 2 * np.sum([f(2 * j) for j in range(1, N_half - 1)])  # type ignore
    )
    return (h / 3) * res
