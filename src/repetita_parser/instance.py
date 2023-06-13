from os import PathLike
from typing import List

import numpy as np

from repetita_parser import demands, topology


def _build_tm(topology: topology.Topology, demands: List[demands.Demand]) -> np.ndarray:
    """
    Per the format specification, demands between the same node pair can occur
    multiple times. This function collapses the list of demands into a
    two-dimensional traffic matrix that sums all demands between any given pair
    into a single value.
    """
    num_nodes = len(topology.nodes)
    tm = np.zeros(shape=(num_nodes, num_nodes))

    for d in demands:
        tm[d.src, d.dest] += d.bandwidth

    return tm


class Instance:
    def __init__(self, topology_file: PathLike, demands_file: PathLike) -> None:
        self.topology: topology.Topology = topology.parse(topology_file)
        self.demands: List[demands.Demand] = demands.parse(demands_file)

        self.traffic_matrix = _build_tm(self.topology, self.demands)
        """
        Total traffic demand from node `i` to node `j` at `traffic_matrix[i, j]`
        """
