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

    def bearing_capacity(self, f_tot: float = 1.0) -> float:
        return (self.shaft_friction() + self.tip_resistance()) / f_tot

    def shaft_friction(self) -> float:
        tau = lambda z: (self.soil_profile.pp_eff(z) + self.soil_profile.a)
        return (
            self.pile.shear_ratio
            * simpson(tau, 0, self.pile.length, 10)
            * self.pile.perimeter()
        )

    def tip_resistance(self) -> float:
        sigma_pm = (self.soil_profile.Nq - 1) * (
            self.soil_profile.pp_eff(self.pile.length) + self.soil_profile.a
        )
        return self.pile.area() * sigma_pm


# Some bug in scipy/numpy means we need an explicit integral function
def simpson(f, a, b, N_half=10):
    h = (b - a) / (2 * N_half)
    res = (
        f(a)
        + f(b)
        + 4 * np.sum([f(2 * j - 1) for j in range(1, N_half)])  # type ignore
        + 2 * np.sum([f(2 * j) for j in range(1, N_half - 1)])  # type ignore
    )
    return (h / 3) * res
