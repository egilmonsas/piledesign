from dataclasses import dataclass

import numpy as np

from piledesign.bearing_capacity import SolverType
from piledesign.bearing_capacity.ngi99 import NGI99
from piledesign.bearing_capacity.nordal import Nordal
from piledesign.gis import Coordinate
from piledesign.material import Material, MaterialType, material_preset
from piledesign.soil import SoilProfile


@dataclass
class Pile:
    _PI = 3.14159265359
    _g = 9.82

    def __init__(
        self,
        pos: Coordinate,
        diameter: float,
        length: float,
        material: Material = material_preset(MaterialType.WOOD),
        roughness_ratio: float = -0.9,
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
        self.length = length + 0.1  ### SHIT SOLUTION PLEASE FIX
        self.roughness_ratio = roughness_ratio
        self.material = material

    def weight(self):
        return self.volume() * self.material.density * self._g / 1000

    def volume(self):
        return self.area() * self.length

    def section_capacity(self) -> float:
        return np.clip(self.area() * self.material.f_compressive * 1000.0, 0.01, None)

    def section_utilization(self, N) -> float:
        return N / self.section_capacity()

    def utilization(
        self, solver_type: SolverType, N, soil: SoilProfile, gamma_tot: float = 1.1
    ) -> float:
        return N / self.bearing_capacity(solver_type, soil, gamma_tot)

    def bearing_capacity(
        self, solvertype: SolverType, soil: SoilProfile, gamma_tot: float = 1.1
    ) -> float:
        s = Nordal(self, soil)
        match solvertype:
            case SolverType.NORDAL:
                s = Nordal(self, soil)
            case SolverType.NGI99:
                s = NGI99(self, soil)
        return s.bearing_capacity() / gamma_tot - self.weight()

    def area(self) -> float:
        return self._PI / 4 * self.diameter**2

    def perimeter(self) -> float:
        return self._PI * self.diameter
