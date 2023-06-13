import pytest
from paths import DEMANDS_FILE_PATH, TOPOLOGY_FILE_PATH

from repetita_parser.instance import Instance


def test_instance():
    i = Instance(TOPOLOGY_FILE_PATH, DEMANDS_FILE_PATH)

    pytest.approx(26364.0, i.traffic_matrix[0, 1])
