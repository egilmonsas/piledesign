from piledesign.pile import Pile
from piledesign.soil import SoilProfile


class NGI99:
    def __init__(self, pile:Pile,soil_profile:SoilProfile) -> None:
        self.soil_profile = soil_profile
        self.pile = pile
    
    def test(self):
        print(self.soil_profile.pp_eff(4))