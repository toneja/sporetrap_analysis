#!/usr/bin/env python3
#
# This file is part of the sporetrap analysis scripts.
#
# Copyright (c) 2025 Jason Toney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Scatter plot the microsphere counts: manual counts vs. automated counts"""

import os
import sys
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt


def linear_fx(x, slope, intercept):
    """Linear function: y = mx + b"""
    return slope * x + intercept


def plot_particles(excel_file, color, show_plot=False):
    """Plot manual vs. automated microsphere counts."""
    # Set up the data frame
    data = pd.read_excel(excel_file)
    df = pd.DataFrame(data)
    x = df[f"{color} (manual)"]
    y = df[f"{color} (SW)"]
    # Fit the function to the data and score the fit
    popt, _ = curve_fit(linear_fx, x, y)  # pylint: disable=unbalanced-tuple-unpacking
    fitted = linear_fx(x, *popt)
    r2 = round(r2_score(y, fitted), 3)
    # Scatter plot the data
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color="black", marker="o")
    plt.axline((0, 0), slope=1, color="black", linestyle="--")
    plt.xlabel("Manual Counts")
    plt.ylabel("Automated Technique")
    if color == "Green":
        size = 33
    else:
        size = 165
    plt.title(f"{color} Microspheres ({size} μm) 1:1 Scatter (R$^2$ = {r2})")
    # Save a copy of the plot
    plt.savefig(
        f"Scatter_Manual_Automated_{size}_Micron.png", dpi=300, bbox_inches="tight"
    )
    # Only display the plot when wanted
    if show_plot:
        plt.show()
    plt.close()


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    if len(sys.argv) > 1:
        plot_particles(sys.argv[1], "Green", len(sys.argv) > 2)
        plot_particles(sys.argv[1], "Red", len(sys.argv) > 2)
    else:
        plot_particles("ACDC - manual counts.xlsx", "Green", True)
        plot_particles("ACDC - manual counts.xlsx", "Red", True)
