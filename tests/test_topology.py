from pathlib import Path

import pytest
from paths import TOPOLOGY_FILE_PATH

from repetita_parser import topology
from repetita_parser.errors import ParseError


def test_parse():
    topo = topology.parse(TOPOLOGY_FILE_PATH)
    assert len(topo.nodes) == 30
    assert len(topo.edges) == 110


def test_networkx():
    topo = topology.parse(TOPOLOGY_FILE_PATH)
    g = topo.as_nx_graph()

    assert g.number_of_nodes() == 30
    assert g.number_of_edges() == 110


def test_no_networkx():
    topology._has_networkx = False

    topo = topology.parse(TOPOLOGY_FILE_PATH)

    with pytest.raises(ImportError, match="NetworkX is required to call this function"):
        topo.as_nx_graph()

    topology._has_networkx = True


def test_parse_errors():
    root = Path("tests/data/bad")

    with pytest.raises(ParseError, match="expected nodes header line"):
        topology.parse(root / "bad_node_header.graph")

    with pytest.raises(ParseError, match="expected nodes memo line"):
        topology.parse(root / "bad_node_memo.graph")

    with pytest.raises(ParseError, match="not all node fields present"):
        topology.parse(root / "bad_node_fields.graph")

    with pytest.raises(ParseError, match="expected edges header line"):
        topology.parse(root / "bad_edge_header.graph")

    with pytest.raises(ParseError, match="expected edges memo line"):
        topology.parse(root / "bad_edge_memo.graph")

    with pytest.raises(ParseError, match="not all edge fields present"):
        topology.parse(root / "bad_edge_fields.graph")
