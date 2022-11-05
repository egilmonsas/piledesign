from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

from piledesign import pile, soil


def draw_capacity_diagram(
    s, d_range: Tuple[float, float], L_range: Tuple[float, float]
):
    def f(s, d, L):
        p = pile.Pile(d, L)
        return p.bearing_capacity(s, f_tot=1.35)

    def fa(s, d, L):
        p = pile.Pile(d, L)
        return p.section_capacity()

    d = np.linspace(d_range[0], d_range[1])
    L = np.linspace(L_range[0], L_range[1])
    X, Y = np.meshgrid(d, L)
    Z = f(s, X, Y)
    Za = fa(s, X, Y)

    lines = [
        200,
        300,
        400,
        500,
        600,
        800,
        1000,
        1250,
        1500,
        2000,
        3000,
        5000,
        7500,
        10000,
    ]
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.clabel(ax.contour(X, Y, Za, lines, colors="red"), inline=True, fontsize=8)
    ax.clabel(ax.contour(X, Y, Z, lines, colors="black"), inline=True, fontsize=8)
    ax.yaxis.set_inverted(True)
    ax.xaxis.tick_top()
    return fig


def draw_utilization_diagram(
    N, s, d_range: Tuple[float, float], L_range: Tuple[float, float]
):
    def f(N, s, d, L):
        p = pile.Pile(d, L)
        return p.utilization(N, s, f_tot=1.35)

    def fa(N, d, L):
        p = pile.Pile(d, L)
        return p.section_utilization(N)

    d = np.linspace(d_range[0], d_range[1])
    L = np.linspace(L_range[0], L_range[1])
    X, Y = np.meshgrid(d, L)
    Z = f(N, s, X, Y)
    Za = fa(N, X, Y)

    fig, ax = plt.subplots()
    ax.grid(True)
    ax.clabel(
        ax.contour(X, Y, Z, np.round(np.linspace(0, 1, 11), 1), colors="black"),
        inline=True,
        fontsize=8,
    )
    ax.clabel(
        ax.contour(X, Y, Za, np.round(np.linspace(0, 1, 11), 1), colors="red"),
        inline=True,
        fontsize=8,
    )
    ax.yaxis.set_inverted(True)
    ax.xaxis.tick_top()
    return fig


def draw_soil_stress(s, L_range: Tuple[float, float]):
    L = np.linspace(L_range[0], L_range[1])

    fig, ax = plt.subplots()
    ax.grid(True)
    ax.plot(s.pp(L), L, color="black", linestyle="dashed")
    ax.plot(s.pp_eff(L), L, color="black")
    ax.yaxis.set_inverted(True)
    ax.xaxis.tick_top()
    return fig


def draw_cpt(cpt, L_range: Tuple[float, float]):
    L = np.linspace(L_range[0], L_range[1])

    fig, ax = plt.subplots()
    ax.grid(True)
    ax.plot(cpt.qc(L), L, color="black")
    ax.yaxis.set_inverted(True)
    ax.set_xlim(0, ax.get_xlim()[1])
    ax.xaxis.tick_top()
    return fig
