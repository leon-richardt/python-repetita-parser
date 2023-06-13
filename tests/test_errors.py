from pathlib import Path

from repetita_parser.errors import ParseError


def test_str_rep():
    only_msg = ParseError("message")
    assert str(only_msg) == "message"

    dummy_path = Path("foo/file.txt")
    msg_and_fp = ParseError("message", dummy_path)
    assert str(msg_and_fp) == "foo/file.txt: message"

    msg_fp_ln = ParseError("message", dummy_path, 1)
    assert str(msg_fp_ln) == "foo/file.txt:1: message"
