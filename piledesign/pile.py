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

    def __init__(
        self,
        pos: Coordinate,
        diameter: float,
        length: float,
        material: Material = material_preset(MaterialType.WOOD),
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
        self.shear_ratio = 0.3
        self.material = material

    def weight(self):
        return self.volume() * self.material.density

    def volume(self):
        return self.area() * self.length

    def section_capacity(self) -> float:
        return np.clip(self.area() * self.material.f_compressive * 1000.0, 0.01, None)

    def section_utilization(self, N) -> float:
        return N / self.section_capacity()

    def utilization(
        self, solver_type: SolverType, N, soil: SoilProfile, f_tot: float = 1.0
    ) -> float:
        return N / self.bearing_capacity(solver_type, soil, f_tot)

    def bearing_capacity(
        self, solvertype: SolverType, soil: SoilProfile, f_tot: float = 1.0
    ) -> float:
        s = Nordal(self, soil)
        match solvertype:
            case SolverType.NORDAL:
                s = Nordal(self, soil)
            case SolverType.NGI99:
                s = NGI99(self, soil)
        return s.bearing_capacity() - self.weight()

    def area(self) -> float:
        return self._PI / 4 * self.diameter**2

    def perimeter(self) -> float:
        return self._PI * self.diameter
