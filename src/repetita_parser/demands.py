from typing import List, NamedTuple

from repetita_parser.errors import ParseError
from repetita_parser.types import PathLike


class Demand(NamedTuple):
    label: str
    src: int
    dest: int
    bandwidth: float


def parse(file_path: PathLike) -> List[Demand]:
    demands_id = "DEMANDS"
    memo_line = "label src dest bw\n"
    num_header_fields = 2
    num_demand_fields = 4

    demands: List[Demand] = []

    with open(file_path) as f:
        for line_idx, line in enumerate(f.readlines()):
            fields = line.strip("\n").split()

            if line_idx == 0:
                if len(fields) != num_header_fields or fields[0] != demands_id:
                    msg = "expected demands header line"
                    raise ParseError(msg, file_path, line_idx + 1)
            elif line_idx == 1:
                if line != memo_line:
                    msg = "expected demands memo line"
                    raise ParseError(msg, file_path, line_idx + 1)
            else:
                if len(fields) != num_demand_fields:
                    msg = "not all demand fields present"
                    raise ParseError(msg, file_path, line_idx + 1)

                label = fields[0]
                src = int(fields[1])
                dest = int(fields[2])
                bw = float(fields[3])

                demands.append(Demand(label, src, dest, bw))

    return demands
