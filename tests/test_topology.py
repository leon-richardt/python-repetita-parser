from pathlib import Path

import pytest
from paths import EXPORT_TOPOLOGY_FILE_PATH, TOPOLOGY_FILE_PATH

from repetita_parser import errors, topology


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


def test_export():
    # NOTE: Depends on `Topology.parse()` being correct
    ground_truth_topo = topology.parse(TOPOLOGY_FILE_PATH)
    with open(EXPORT_TOPOLOGY_FILE_PATH, "w") as f:
        ground_truth_topo.export(f)

    import_topo = topology.parse(EXPORT_TOPOLOGY_FILE_PATH)

    assert ground_truth_topo == import_topo

    # This line is for coverage of `Topology.__ne__()`
    assert not (ground_truth_topo != import_topo)


bad_root = Path("tests/data/parsing/bad")


@pytest.mark.parametrize(
    "topo_file, expectation",
    [
        (
            bad_root / "bad_node_header.graph",
            pytest.raises(errors.ParseError, match="expected nodes header line"),
        ),
        (bad_root / "bad_node_memo.graph", pytest.raises(errors.ParseError, match="expected nodes memo line")),
        (bad_root / "bad_node_fields.graph", pytest.raises(errors.ParseError, match="not all node fields present")),
        (bad_root / "bad_edge_header.graph", pytest.raises(errors.ParseError, match="expected edges header line")),
        (bad_root / "bad_edge_memo.graph", pytest.raises(errors.ParseError, match="expected edges memo line")),
        (bad_root / "bad_edge_fields.graph", pytest.raises(errors.ParseError, match="not all edge fields present")),
    ],
)
def test_parse_errors(topo_file, expectation):
    with expectation:
        topology.parse(topo_file)
