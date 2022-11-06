from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from piledesign.pile import Pile

import numpy as np

from piledesign.soil import SoilProfile


class Nordal:
    def __init__(self, pile: Pile, soil_profile: SoilProfile) -> None:
        self.pile = pile
        self.soil_profile = soil_profile
