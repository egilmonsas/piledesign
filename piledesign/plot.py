from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

from piledesign import pile, soil
from piledesign.bearing_capacity import SolverType
from piledesign.gis import Coordinate


def draw_capacity_diagram(
    solver_type: SolverType,
    s,
    p,
    d_range: Tuple[float, float],
    L_range: Tuple[float, float],
):
    def f(s, p, d, L):
        p.diameter = d
        p.length = L
        return p.bearing_capacity(solver_type, s, gamma_tot=1.45 / 1.1)

    def fa(s, p, d, L):
        p.diameter = d
        p.length = L
        return p.section_capacity()

    d = np.linspace(d_range[0], d_range[1])
    L = np.linspace(L_range[0], L_range[1])
    X, Y = np.meshgrid(d, L)
    Z = f(s, p, X, Y)
    Za = fa(s, p, X, Y)

    lines = [
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
    ax.contour(X, Y, Za - Z, [0], colors="green")
    ax.yaxis.set_inverted(True)
    ax.xaxis.tick_top()
    return fig


def draw_utilization_diagram(
    solver_type: SolverType,
    N,
    s,
    p,
    d_range: Tuple[float, float],
    L_range: Tuple[float, float],
):
    def f(N, s, p, d, L):
        p.diameter = d
        p.length = L
        return p.utilization(solver_type, N, s, gamma_tot=1.45 / 1.1)

    def fa(N, s, p, d, L):
        p.diameter = d
        p.length = L
        return p.section_utilization(N)

    d = np.linspace(d_range[0], d_range[1])
    L = np.linspace(L_range[0], L_range[1])
    X, Y = np.meshgrid(d, L)
    Z = f(N, s, p, X, Y)
    Za = fa(N, s, p, X, Y)

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
    ax.contour(X, Y, Za - Z, [0], colors="green")

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
