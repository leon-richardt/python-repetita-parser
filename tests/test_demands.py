from pathlib import Path

import pytest
from paths import DEMANDS_FILE_PATH

from repetita_parser import demands, errors


def test_parse():
    d = demands.parse(DEMANDS_FILE_PATH)
    assert len(d.list) == 870


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
