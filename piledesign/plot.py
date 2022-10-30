from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

import pile
import soil


def f(s,d, L):
    p = pile.Pile(d,L)
    return p.bearing_capacity(s)

def draw_capacity_diagram(p,s,d_range:Tuple[float,float],L_range:Tuple[float,float]):
    d = np.linspace(d_range[0],d_range[1])
    L = np.linspace(L_range[0],L_range[1])
    X, Y = np.meshgrid(d, L)
    Z = f(s,X, Y)

    fig, ax =  plt.subplots()
    ax.grid(True)
    ax.clabel(ax.contour(X,Y, Z,20, colors='black'), inline=True, fontsize=8)
    ax.yaxis.set_inverted(True)
    return fig

def draw_soil_stress(s,L_range:Tuple[float,float]):
    L = np.linspace(L_range[0],L_range[1])

    fig, ax =  plt.subplots()
    ax.grid(True)
    ax.plot(s.pp(L),L,color="black",linestyle="dashed")
    ax.plot(s.pp_eff(L),L,color="black")
    ax.yaxis.set_inverted(True)
    return fig

def draw_cpt(cpt,L_range:Tuple[float,float]):
    L = np.linspace(L_range[0],L_range[1])

    fig, ax =  plt.subplots()
    ax.grid(True)
    ax.plot(cpt.qc(L),L,color="black")
    ax.yaxis.set_inverted(True)
    ax.set_xlim(0, ax.get_xlim()[1])
    return fig
