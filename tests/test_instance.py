from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pytest
from paths import DEMANDS_FILE_PATH, TOPOLOGY_FILE_PATH

from repetita_parser import errors
from repetita_parser.instance import Instance


def test_instance():
    i = Instance(TOPOLOGY_FILE_PATH, DEMANDS_FILE_PATH)

    pytest.approx(26364.0, i.traffic_matrix[0, 1])


bad_root = Path("tests/data/validation/bad")


@pytest.mark.parametrize(
    "topo_file, demand_file, expectation",
    [
        (TOPOLOGY_FILE_PATH, DEMANDS_FILE_PATH, does_not_raise()),
        (
            TOPOLOGY_FILE_PATH,
            bad_root / "src_bad.demands",
            pytest.raises(errors.ValidationError, match="demand src_bad:"),
        ),
        (
            TOPOLOGY_FILE_PATH,
            bad_root / "dest_bad.demands",
            pytest.raises(errors.ValidationError, match="demand dest_bad:"),
        ),
        (
            TOPOLOGY_FILE_PATH,
            bad_root / "both_bad.demands",
            pytest.raises(errors.ValidationError, match="demand both_bad:"),
        ),
    ],
)
def test_validation(topo_file, demand_file, expectation):
    with expectation:
        Instance(topo_file, demand_file)
