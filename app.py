import random

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from piledesign import cpt, pile, plot, soil
from piledesign.bearing_capacity import SolverType
from piledesign.bearing_capacity.ngi99 import NGI99
from piledesign.gis import Coordinate

# Inputwidgets
with st.sidebar:
    with st.expander("Pel", True):
        d = st.slider("Diameter", 0.1, 2.0, (0.1, 0.5), 0.05)
        L = st.slider("Lengde", 0, 30, (0, 30), 1)
    with st.expander("CPT-profil", False):
        qc_0 = st.number_input("Spissmotstand z=0", 0, 10000, 5000, 100)
        qc_z = st.number_input("Spissmotstand stigning", 0, 1000, 330, 10)
    with st.expander("Jordprofil", True):
        density = st.number_input("Romvekt", 0.0, 30.0, 20.0, 0.5)
        with st.container():
            phi = st.number_input("Friksjonsvinkel", 5, 60, 35, 1)
            tanphi = st.text(
                f"tan(phi) {np.tan(np.deg2rad(phi)):.3f} | tan(rho) {np.tan(np.deg2rad(phi))/1.4:.3f}"
            )
        ground_water = st.number_input("GVS", None, None, 6.0, 0.5)
        Nq = st.number_input("Nq", 1, 1000, 30, 1)
        Nq_graph = st.image(Image.open("assets\\Nq.png"))
    with st.expander("Last", False):
        N = st.number_input("Aksiallast [kN]", 0, None, 500, 10)
# Setup
origin = Coordinate(0, 0)

p = pile.Pile(origin, d[1], L[1])
s = soil.SoilProfile(
    density,
    ground_water_depth=ground_water,
    cpts=[
        cpt.CPT(
            pos=Coordinate(random.randrange(-100, 100), random.randrange(-100, 100)),
            qc_0=random.randrange(3000, 5000),
            qc_z=random.randrange(250, 350),
        )
        for _ in range(5)
    ],
)
ngi99 = NGI99(p, s)
c = ngi99.get_interpolated_cpt()

# Plots and layout
solver_choice = st.selectbox("Løsningsmetode", ("NORDAL", "NGI99"))
solver = SolverType(solver_choice)
tb_soil, tb_cpt, tb_cap, tb_uti = st.tabs(["Jord", "CPT", "Kapasitet", "Utnyttelse"])
with tb_soil:
    st.pyplot(fig=plot.draw_soil_stress(s, L))
with tb_cpt:
    st.pyplot(fig=plot.draw_cpt(c, L))
with tb_cap:
    st.pyplot(fig=plot.draw_capacity_diagram(solver, s, d, L))
with tb_uti:
    st.pyplot(fig=plot.draw_utilization_diagram(solver, N, s, d, L))
