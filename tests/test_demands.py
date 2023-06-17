from pathlib import Path

import pytest
from paths import DEMANDS_FILE_PATH

from repetita_parser import demands
from repetita_parser.errors import ParseError


def test_parse():
    d = demands.parse(DEMANDS_FILE_PATH)
    assert len(d) == 870


def test_parse_errors():
    root = Path("tests/data/parsing/bad")

    with pytest.raises(ParseError, match="expected demands header line"):
        demands.parse(root / "bad_header.demands")

    with pytest.raises(ParseError, match="expected demands memo line"):
        demands.parse(root / "bad_memo.demands")

    with pytest.raises(ParseError, match="not all demand fields present"):
        demands.parse(root / "bad_fields.demands")
