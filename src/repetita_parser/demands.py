from dataclasses import dataclass
from io import TextIOBase
from typing import List

from repetita_parser.errors import ParseError
from repetita_parser.types import PathLike

DEMANDS_ID = "DEMANDS"
DEMANDS_MEMO_LINE = "label src dest bw\n"


@dataclass
class Demand:
    label: str
    src: int
    dest: int
    bandwidth: float


class Demands:
    """
    Wrapper object for demands. Use `Demands.list` to get access to the
    actual `Demand` objects.
    """

    def __init__(self, demands: List[Demand], source_file: PathLike) -> None:
        self.list = demands

        self.source_file = source_file

    def export(self, target: TextIOBase) -> None:
        target.writelines(
            [
                f"{DEMANDS_ID} {len(self.list)}\n",
                DEMANDS_MEMO_LINE,
            ]
        )

        target.writelines([f"{d.label} {d.src} {d.dest} {d.bandwidth}\n" for d in self.list])

    def __eq__(self, other) -> bool:
        """
        Comparison for equality is only defined in terms of the demands
        themselves , i.e., two instances can be equal although their source
        files differ.
        """
        return self.list == other.list

    def __ne__(self, other) -> bool:
        """
        Comparison for equality is only defined in terms of the demands
        themselves , i.e., two instances can be equal although their source
        files differ.
        """
        return not (self.list == other.list)


def parse(file_path: PathLike) -> Demands:
    num_demand_fields = 4
    # If this changes, we have to touch the impl
    assert num_demand_fields == len(DEMANDS_MEMO_LINE.strip().split(" "))

    demands: List[Demand] = []

    with open(file_path) as f:
        for line_idx, line in enumerate(f.readlines()):
            fields = line.strip("\n").split()

            if line_idx == 0:
                # Two fields: `DEMANDS_ID` and number of demands
                num_header_fields = 2
                if len(fields) != num_header_fields or fields[0] != DEMANDS_ID:
                    msg = "expected demands header line"
                    raise ParseError(msg, file_path, line_idx + 1)
            elif line_idx == 1:
                if line != DEMANDS_MEMO_LINE:
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

    return Demands(demands, file_path)
