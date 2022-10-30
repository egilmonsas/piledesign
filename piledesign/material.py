from dataclasses import dataclass


@dataclass
class Material:
    density:float
    f_tensile:float
    f_compressive:float
