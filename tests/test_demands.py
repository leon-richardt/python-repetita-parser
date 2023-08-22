from pathlib import Path

import pytest
from paths import DEMANDS_FILE_PATH, EXPORT_DEMANDS_FILE_PATH

from repetita_parser import demands, errors


def test_parse():
    d = demands.parse(DEMANDS_FILE_PATH)
    assert len(d.list) == 870


def test_export():
    # NOTE: Depends on `Topology.parse()` being correct
    ground_truth_dems = demands.parse(DEMANDS_FILE_PATH)
    with open(EXPORT_DEMANDS_FILE_PATH, "w") as f:
        ground_truth_dems.export(f)

    import_dems = demands.parse(EXPORT_DEMANDS_FILE_PATH)

    assert ground_truth_dems == import_dems

    # This line is for coverage of `Topology.__ne__()`
    assert not (ground_truth_dems != import_dems)


bad_root = Path("tests/data/parsing/bad")


@pytest.mark.parametrize(
    "demands_file, expectation",
    [
        (bad_root / "bad_header.demands", pytest.raises(errors.ParseError, match="expected demands header line")),
        (bad_root / "bad_memo.demands", pytest.raises(errors.ParseError, match="expected demands memo line")),
        (bad_root / "bad_fields.demands", pytest.raises(errors.ParseError, match="not all demand fields present")),
    ],
)
def test_parse_errors(demands_file, expectation):
    with expectation:
        demands.parse(demands_file)
