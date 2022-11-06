from dataclasses import dataclass

from piledesign.gis import Coordinate  # type: ignore


@dataclass
class CPT:
    pos: Coordinate
    qc_0: float
    qc_z: float

    def qc(self, depth: float) -> float:
        return self.qc_0 + self.qc_z * depth
