from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pytest
from paths import DEMANDS_FILE_PATH, EXPORT_INSTANCE_DIR, TOPOLOGY_FILE_PATH

from repetita_parser import errors
from repetita_parser.instance import Instance


def test_instance():
    i = Instance(TOPOLOGY_FILE_PATH, DEMANDS_FILE_PATH)

    pytest.approx(26364.0, i.traffic_matrix[0, 1])


def test_export():
    ground_truth = Instance(TOPOLOGY_FILE_PATH, DEMANDS_FILE_PATH)

    topo_target = EXPORT_INSTANCE_DIR / "exported.graph"
    dems_target = EXPORT_INSTANCE_DIR / "exported.demands"

    with open(topo_target, "w") as tf:
        with open(dems_target, "w") as df:
            ground_truth.export(tf, df)

    imported = Instance(topo_target, dems_target)

    assert ground_truth == imported

    # For coverage
    assert not (ground_truth != imported)


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
