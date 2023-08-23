import io
from dataclasses import dataclass
from typing import List

from repetita_parser.errors import ParseError
from repetita_parser.types import PathLike

try:
    import networkx as nx
except ImportError:
    _has_networkx = False
else:
    _has_networkx = True

NODES_ID = "NODES"
EDGES_ID = "EDGES"
NODES_MEMO_LINE = "label x y\n"
EDGES_MEMO_LINE = "label src dest weight bw delay\n"


@dataclass
class Node:
    label: str
    x: float
    y: float


@dataclass
class Edge:
    label: str
    src: int
    dest: int
    weight: float
    bandwidth: float
    delay: float


class Topology:
    def __init__(self, nodes: List[Node], edges: List[Edge], source_file: PathLike) -> None:
        self.nodes: List[Node] = nodes
        self.edges: List[Edge] = edges

        self.source_file = source_file

    def __eq__(self, other) -> bool:
        """
        Comparison for equality is only defined in terms of the topology
        structure, i.e., two instances can be equal although their source files
        differ.
        """
        return all(
            [
                self.nodes == other.nodes,
                self.edges == other.edges,
            ]
        )

    def __ne__(self, other) -> bool:
        """
        Comparison for equality is only defined in terms of the topology
        structure, i.e., two instances can be equal although their source files
        differ.
        """
        return not (self == other)

    def as_nx_graph(self):
        """
        Convert the topology to a `networkx.MultiDiGraph`. In the graph, nodes
        are represented by their index into `self.nodes`. Node and edge objects
        carry their respective `Node` and `Edge` objects in their attributes
        under the `obj` key.

        This function requires NetworkX to be installed. If you call this
        function without NetworkX available, it will raise an ImportError.
        """

        if not _has_networkx:
            msg = "NetworkX is required to call this function"
            raise ImportError(msg)
        else:
            graph = nx.MultiDiGraph()
            for node_idx, node in enumerate(self.nodes):
                graph.add_node(node_idx, obj=node)

            for edge in self.edges:
                graph.add_edge(edge.src, edge.dest, obj=edge)

            return graph

    def export(self, target: io.TextIOBase) -> None:
        # Write node info
        target.writelines(
            [
                f"{NODES_ID} {len(self.nodes)}\n",
                NODES_MEMO_LINE,
            ]
        )

        target.writelines([f"{n.label} {n.x} {n.y}\n" for n in self.nodes])
        target.write("\n")

        # Write edge info
        target.writelines(
            [
                f"{EDGES_ID} {len(self.edges)}\n",
                EDGES_MEMO_LINE,
            ]
        )

        target.writelines([f"{e.label} {e.src} {e.dest} {e.weight} {e.bandwidth} {e.delay}\n" for e in self.edges])


@dataclass
class _ParserState:
    stream: io.TextIOWrapper
    file_path: PathLike
    line_idx: int

    @property
    def line_num(self) -> int:
        return self.line_idx + 1


def _parse_nodes(state: _ParserState) -> List[Node]:
    num_node_fields = 3
    # If this changes, we have to touch the impl
    assert len(NODES_MEMO_LINE.strip().split(" ")) == num_node_fields

    nodes: List[Node] = []

    # Nodes and edges are separated by a blank line
    while (line := state.stream.readline()) != "\n":
        fields = line.strip("\n").split()

        if state.line_idx == 1:
            if line != NODES_MEMO_LINE:
                msg = "expected nodes memo line"
                raise ParseError(msg, state.file_path, state.line_num)
        elif len(fields) != num_node_fields:
            msg = "not all node fields present"
            raise ParseError(msg, state.file_path, state.line_num)
        else:
            label = fields[0]
            x = float(fields[1])
            y = float(fields[2])

            nodes.append(Node(label, x, y))

        state.line_idx += 1

    state.line_idx += 1
    return nodes


def _parse_edges(state: _ParserState) -> List[Edge]:
    num_edge_fields = 6
    # If this changes, we have to touch the impl
    assert num_edge_fields == len(EDGES_MEMO_LINE.strip().split(" "))

    edges: List[Edge] = []

    start_line_idx = state.line_idx
    # At EOF, we read an empty string which is falsey
    while line := state.stream.readline():
        fields = line.strip("\n").split()

        if state.line_idx == start_line_idx:
            if line != EDGES_MEMO_LINE:
                msg = "expected edges memo line"
                raise ParseError(msg, state.file_path, state.line_num)
        else:
            if len(fields) != num_edge_fields:
                msg = "not all edge fields present"
                raise ParseError(msg, state.file_path, state.line_num)

            label = fields[0]
            src = int(fields[1])
            dest = int(fields[2])
            weight = float(fields[3])
            bw = float(fields[4])
            delay = float(fields[5])

            edges.append(Edge(label, src, dest, weight, bw, delay))

        state.line_idx += 1

    state.line_idx += 1
    return edges


def parse(file_path: PathLike) -> Topology:
    with open(file_path) as f:
        cur_line_idx = 0
        line = f.readline()
        fields = line.strip("\n").split()

        if fields[0] != NODES_ID:
            msg = "expected nodes header line"
            raise ParseError(msg, file_path, cur_line_idx + 1)

        cur_line_idx += 1
        state = _ParserState(f, file_path, cur_line_idx)
        nodes = _parse_nodes(state)

        line = f.readline()
        state.line_idx += 1
        fields = line.strip("\n").split()

        if fields[0] != EDGES_ID:
            msg = "expected edges header line"
            raise ParseError(msg, file_path, cur_line_idx + 1)

        edges = _parse_edges(state)

        return Topology(nodes, edges, file_path)
