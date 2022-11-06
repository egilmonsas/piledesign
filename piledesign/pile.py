from dataclasses import dataclass

import numpy as np

from piledesign.bearing_capacity import SolverType
from piledesign.bearing_capacity.ngi99 import NGI99
from piledesign.bearing_capacity.nordal import Nordal
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
        self.length = length + 1  ### SHIT SOLUTION PLEASE FIX
        self.shear_ratio = 0.3
        self.material = Material(500, 7, 9)

    def utilization(self,solver_type:SolverType, N, soil: SoilProfile, f_tot: float = 1.0) -> float:
        return N / self.bearing_capacity(solver_type, soil, f_tot)

    def section_capacity(self) -> float:
        return np.clip(self.area() * self.material.f_compressive * 1000, 0.01, None)

    def section_utilization(self, N) -> float:
        return N / self.section_capacity()

    def bearing_capacity(
        self, solvertype: SolverType, soil: SoilProfile, f_tot: float = 1.0
    ) -> float:
        s = Nordal(self, soil)
        match solvertype:
            case SolverType.NORDAL:
                s = Nordal(self, soil)
            case SolverType.NGI99:
                s = NGI99(self, soil)
        return s.bearing_capacity()

    def area(self) -> float:
        return self._PI / 4 * self.diameter**2

    def perimeter(self) -> float:
        return self._PI * self.diameter
