from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from typing_extensions import Self


class MaterialType(Enum):
    STEEL = "STEEL"
    CONCRETE = "CONCRETE"
    WOOD = "WOOD"


@dataclass
class Material:
    density: float
    f_tensile: float
    f_compressive: float


def material_preset(material_type: MaterialType) -> Material:
    match material_type:
        case MaterialType.STEEL:
            return Material(7000, 311, 311)
        case MaterialType.CONCRETE:
            return Material(2400, 5, 30)
        case MaterialType.WOOD:
            return Material(900, 5, 8)
        case _:
            raise NotImplementedError("Couldnt find material")
