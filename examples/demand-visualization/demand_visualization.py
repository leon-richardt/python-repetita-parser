import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns

from repetita_parser.instance import Instance


def get_sorted_demands(instance):
    return np.flip(np.sort(instance.traffic_matrix.flatten()))


def get_cum_demands(instance):
    sorted_demands = get_sorted_demands(instance)
    total_traffic = sorted_demands.sum()
    relative_demands = sorted_demands / total_traffic
    return np.cumsum(relative_demands)


def plot(instance):
    sorted_demands = get_sorted_demands(instance)
    cum_demands = get_cum_demands(instance)

    ranks = np.array(range(1, len(sorted_demands) + 1))

    fig, axes = plt.subplot_mosaic(
        """
        CAA
        CAA
        EBD
        EBD
    """
    )

    sns.kdeplot(x=sorted_demands, cut=0, ax=axes["A"])
    sns.rugplot(x=sorted_demands, ax=axes["A"])
    axes["A"].set_title("KDE plot of demand volumes")
    axes["A"].set_xlabel("Demand Volume")

    sns.heatmap(
        instance.traffic_matrix / instance.traffic_matrix.sum(),
        ax=axes["C"],
        square=True,
        cmap="YlGnBu",
        linewidth=0.75,
        cbar_kws={"location": "right"},
    )
    axes["C"].set_title("Demand volumes as share of total traffic")
    axes["C"].set_xlabel("Destination Node Index")
    axes["C"].set_ylabel("Source Node Index")

    relative_ranks = ranks / len(ranks)
    axes["B"].plot(relative_ranks, cum_demands)
    axes["B"].set_title("Fraction of total volume covered by top N demands")
    axes["B"].set_xlabel("Demand Rank (quantile)")

    axes["D"].plot(ranks, cum_demands)
    axes["D"].set_title("Fraction of total volume covered by top N demands\n(log-log scale)")
    axes["D"].set_xlabel("Demand Rank (absolute)")
    axes["D"].set_yscale("log")
    axes["D"].set_xscale("log")

    for ax in [axes["B"], axes["D"]]:
        ax.set_ylabel("Fraction covered")

    nx.draw(
        instance.topology.as_nx_graph(),
        node_size=100,
        with_labels=True,
        font_size=8,
        font_color="#f4f4f4",
        ax=axes["E"],
    )
    axes["E"].set_title("Drawing of the network")

    return fig, axes


def main():
    topo_file = Path(sys.argv[1])
    demands_file = Path(sys.argv[2])
    instance = Instance(topo_file, demands_file)

    sns.set_style("whitegrid")
    fig, _ = plot(instance)
    sns.despine()

    def figure_title():
        num_nodes = len(instance.topology.nodes)
        num_edges = len(instance.topology.edges)
        return (
            f"Topology: {topo_file},\n"
            f"Demands: {demands_file}\n"
            f"({num_nodes} nodes, density: {100 * num_edges / num_nodes**2:.2f}%)"
        )

    fig.suptitle(figure_title())

    fig.set_size_inches(16, 9)
    fig.tight_layout()
    fig.savefig("traffic_distribution.pdf", transparent=True)


if __name__ == "__main__":
    main()
