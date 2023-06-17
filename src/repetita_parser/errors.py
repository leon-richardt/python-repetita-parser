from typing import Optional

from repetita_parser.types import PathLike


class ParseError(Exception):
    def __init__(self, message: str, file_path: Optional[PathLike] = None, line_num: Optional[int] = None):
        self.message = message
        self.file_path = file_path
        self.line_num = line_num

    def __str__(self):
        retval = ""

        has_fp: bool = self.file_path is not None
        has_line: bool = self.line_num is not None

        if has_fp:
            retval += str(self.file_path)

        if has_line:
            retval += f":{self.line_num}"

        if has_fp or has_line:
            retval += ": "

        retval += self.message

        return retval


class ValidationError(Exception):
    def __init__(self, message: str, topo_path: PathLike, demands_path: PathLike):
        super().__init__(message)

        self.topo_path = topo_path
        self.demands_path = demands_path
