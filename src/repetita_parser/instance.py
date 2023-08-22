from io import TextIOBase
from os import PathLike
from string import Template

import numpy as np

from repetita_parser import demands, errors, topology


def _build_tm(topology: topology.Topology, demands: demands.Demands) -> np.ndarray:
    """
    Per the format specification, demands between the same node pair can occur
    multiple times. This function collapses the list of demands into a
    two-dimensional traffic matrix that sums all demands between any given pair
    into a single value.
    """
    num_nodes = len(topology.nodes)
    tm = np.zeros(shape=(num_nodes, num_nodes))

    for d in demands.list:
        tm[d.src, d.dest] += d.bandwidth

    return tm


class Instance:
    def __init__(self, topology_file: PathLike, demands_file: PathLike) -> None:
        self.topology: topology.Topology = topology.parse(topology_file)
        self.demands: demands.Demands = demands.parse(demands_file)

        # Check if all indices in parsed demands are valid for parsed topology
        min_node_idx, max_node_idx = 0, len(self.topology.nodes) - 1
        for d in self.demands.list:
            src_ok = min_node_idx <= d.src <= max_node_idx
            dest_ok = min_node_idx <= d.dest <= max_node_idx

            if not (src_ok and dest_ok):
                msg_template = Template(f"demand {d.label}: node index $index does not exist in topology")

                if not src_ok:
                    msg = msg_template.substitute(index=d.src)
                else:
                    msg = msg_template.substitute(index=d.dest)

                # XXX: In theory, both indices could be invalid. In that case,
                #      we only report the invalid source index.

                raise errors.ValidationError(msg, topology_file, demands_file)

        self.traffic_matrix = _build_tm(self.topology, self.demands)
        """
        Total traffic demand from node `i` to node `j` at `traffic_matrix[i, j]`
        """

    def __eq__(self, other) -> bool:
        return all(
            [
                self.topology == other.topology,
                self.demands == other.demands,
            ]
        )

    def __ne__(self, other) -> bool:
        return not (self == other)

    def export(self, topology_target: TextIOBase, demands_target: TextIOBase) -> None:
        self.topology.export(topology_target)
        self.demands.export(demands_target)
