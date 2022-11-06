from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from piledesign.pile import Pile

import numpy as np

from piledesign.cpt import CPT
from piledesign.soil import SoilProfile


class NGI99:
    SIGMA_A = 100

    def __init__(self, pile: Pile, soil_profile: SoilProfile) -> None:
        self.soil_profile = soil_profile
        self.pile = pile

    def bearing_capacity(self, f_tot: float = 1.0) -> float:
        rsk, rsb = self.compute_Rks()

        return (rsk + rsb) / f_tot

    def compute_Rks(self) -> Tuple[float, float]:
        N = 101
        dz = self.pile.length / (N - 1)
        Rsk = 1.0
        Rbk = 1.0
        cpt = self.get_interpolated_cpt()

        for z in np.linspace(0.5, self.pile.length, N):
            qc = cpt.qc(z)
            sigma_v = self.soil_profile.pp_eff(z)
            dr: float = 0.4 * np.log(qc / (22 * (sigma_v * self.SIGMA_A) ** 0.5))
            tau_s_cal: float = (
                z
                / self.pile.length
                * self.SIGMA_A
                * np.product(self._factors(sigma_v, dr))
            )
            Rsk += tau_s_cal * self.pile.perimeter() * dz

            Rbk = 0.8 * qc / (1 + dr**2) * self.pile.area()
        return Rsk, Rbk

    def _factors(self, sigma_v, dr):
        f_dr = 2.1 * (dr - 0.1) ** 1.7
        f_ld = 1.3
        f_tp = 1.6
        f_mt = 1.0
        f_sg = (sigma_v / self.SIGMA_A) ** 0.25
        return f_dr, f_ld, f_tp, f_mt, f_sg

    def get_interpolated_cpt(self) -> CPT:

        sum_weights = 0
        qc_0 = 0
        qc_z = 0

        for cpt in self.soil_profile.cpts:
            weight = 1 / (self.pile.pos.compute_distance(cpt.pos) ** 2 + 0.1)
            # fmt: off
            sum_weights += weight
            qc_0        += weight * cpt.qc_0
            qc_z        += weight * cpt.qc_z
            # fmt: on
        return CPT(self.pile.pos, qc_0 / sum_weights, qc_z / sum_weights)
