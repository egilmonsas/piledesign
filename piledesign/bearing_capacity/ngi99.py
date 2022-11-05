from piledesign.cpt import CPT
from piledesign.pile import Pile
from piledesign.soil import SoilProfile


class NGI99:
    def __init__(self, pile: Pile, soil_profile: SoilProfile) -> None:
        self.soil_profile = soil_profile
        self.pile = pile

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
