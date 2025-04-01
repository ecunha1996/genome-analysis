from collections import OrderedDict

from matplotlib import patches
from matplotlib.ticker import FuncFormatter
from upsetplot import plot, UpSet
import pandas as pd
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['axes.titlesize'] = 8
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": "Arial",
})
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['font.size'] = 8
plt.rcParams['font.family'] = 'Arial'

custom_palette = ["#55A868", "#4C72B0", "#DD8452"]

def main():
    # dsalina = {
    # "A": 5,
    # "B": 1,
    # "C": 30,
    # "D": 4,
    # "E": 1487,
    # "F": 755,
    # "G": 8,
    # "H": 188,
    # "I": 508
    # }
    # ngaditana = {
    # "A": 0,
    # "B": 0,
    # "C": 9,
    # "D": 5,
    # "E": 42,
    # "F": 86,
    # "G": 5,
    # "H": 1551,
    # "I": 0
    # }
    #
    # plutheri = {
    # "A": 0,
    # "B": 0,
    # "C": 9,
    # "D": 50,
    # "E": 1420,
    # "F": 894,
    # "G": 127,
    # "H": 0,
    # "I": 30
    # }

    dsalina = {
        "A": 13,
        "B": 189,
        "C": 508,
        "D": 4,
        "E": 1487,
        "F": 755,
    }
    ngaditana = {
        "A": 5,
        "B": 1551,
        "C": 9,
        "D": 5,
        "E": 42,
        "F": 86,
    }

    plutheri = {
        "A": 127,
        "B": 0,
        "C": 39,
        "D": 50,
        "E": 1420,
        "F": 894,
    }

    species_dict = {
        "A": [r"$\it{D.\ salina}$", r"$\it{N.\ gaditana}$", r"$\it{D.\ lutheri}$"],
        "B": [r"$\it{Dunaliella}$", r"$\it{Nannochloropsis}$", r"$\it{Diacronema}$"],
        "C": [r"$\it{C.\ reinhardtii}$", r"$\it{P.\ tricornutum}$", r"$\it{E.\ huxleyi}$"],
        "D": [r"$\it{C.\ vulgaris}$", r"$\it{C.\ reinhardtii}$", r"$\it{C.\ reinhardtii}$"],
        "E": [r"$\it{A.\ thaliana}$", r"$\it{A.\ thaliana}$", r"$\it{A.\ thaliana}$"],
        "F": ["Any", "Any", "Any"],
        # "G": [r"$\it{Dunaliella\ salina}$", r"$\it{Nannochloropsis\ gaditana}$", r"$\it{Diacronema\ lutheri}$"],
        # "H": [r"$\it{Dunaliella}$", r"$\it{Nannochloropsis}$", r"$\it{Diacronema}$"],
        # "I": [r"$\it{Chlamydomonas\ reinhardtii}$", r"$\it{Chlamydomonas\ reinhardtii}$", r"$\it{Chlamydomonas\ reinhardtii}$"]
    }

    # Create a figure with multiple pie charts in the same figure
    fig, axes = plt.subplots(1, 3, figsize=(20, 3))

    # Data for each pie
    data_list = [dsalina, ngaditana, plutheri]
    titles = [r"$\it{D. salina}$", r"$\it{N. gaditana}$", r"$\it{P. lutheri}$"]

    for i, (ax, title) in enumerate(zip(axes, titles)):
        # Extract the labels for each species based on the corresponding dictionary values
        labels = [species_dict[key][i] for key in data_list[i].keys()]
        values = list(data_list[i].values())

        # Plot pie chart
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title(title)

    plt.subplots_adjust(wspace=0.2)
    plt.tight_layout()
    plt.savefig("../results/annotation_sources.pdf", dpi=1200, format='pdf', bbox_inches='tight')


if __name__ == '__main__':
    main()
