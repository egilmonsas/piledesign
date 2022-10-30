from dataclasses import dataclass


@dataclass
class CPT:
    qc_0:float
    qc_z:float

    def qc(self,depth:float)->float:
        return self.qc_0 + self.qc_z*depth
