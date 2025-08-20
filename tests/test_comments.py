from pathlib import Path

import pytest

from repetita_parser import demands, errors, topology
from repetita_parser.instance import Instance

# Test data paths
comments_root = Path("tests/data/comments")

# Topology test files
TOPOLOGY_NO_COMMENTS = comments_root / "topology_no_comments.graph"
TOPOLOGY_COMMENTS_START = comments_root / "topology_comments_start.graph"
TOPOLOGY_COMMENTS_MIDDLE = comments_root / "topology_comments_middle.graph"
TOPOLOGY_COMMENTS_INTERSPERSED = comments_root / "topology_comments_interspersed.graph"
TOPOLOGY_COMMENTS_END = comments_root / "topology_comments_end.graph"
TOPOLOGY_WHITESPACE_COMMENTS = comments_root / "topology_whitespace_comments.graph"
TOPOLOGY_EMPTY_COMMENTS = comments_root / "topology_empty_comments.graph"
TOPOLOGY_COMMENT_IN_HEADER = comments_root / "topology_comment_in_header.graph"
TOPOLOGY_COMMENT_IN_MEMO = comments_root / "topology_comment_in_memo.graph"

# Demand test files
DEMANDS_NO_COMMENTS = comments_root / "demands_no_comments.demands"
DEMANDS_COMMENTS_START = comments_root / "demands_comments_start.demands"
DEMANDS_COMMENTS_INTERSPERSED = comments_root / "demands_comments_interspersed.demands"
DEMANDS_COMMENTS_END = comments_root / "demands_comments_end.demands"
DEMANDS_WHITESPACE_COMMENTS = comments_root / "demands_whitespace_comments.demands"
DEMANDS_COMMENT_IN_HEADER = comments_root / "demands_comment_in_header.demands"
DEMANDS_COMMENT_IN_MEMO = comments_root / "demands_comment_in_memo.demands"


class TestTopologyComments:
    def test_strict_mode_default(self):
        """Test that default behavior is strict=True"""
        with pytest.raises(errors.ParseError):
            topology.parse(TOPOLOGY_COMMENTS_START)

    def test_strict_mode_explicit_true(self):
        """Test that strict=True explicitly rejects comments"""
        with pytest.raises(errors.ParseError):
            topology.parse(TOPOLOGY_COMMENTS_START, strict=True)

    @pytest.mark.parametrize("topo_file", [
        TOPOLOGY_COMMENTS_START,
        TOPOLOGY_COMMENTS_MIDDLE,
        TOPOLOGY_COMMENTS_INTERSPERSED,
        TOPOLOGY_COMMENTS_END,
        TOPOLOGY_WHITESPACE_COMMENTS,
        TOPOLOGY_EMPTY_COMMENTS,
    ])
    def test_strict_mode_rejects_all_comments(self, topo_file):
        """Test that strict mode rejects all types of comments"""
        with pytest.raises(errors.ParseError):
            topology.parse(topo_file, strict=True)

    @pytest.mark.parametrize("topo_file", [
        TOPOLOGY_COMMENTS_START,
        TOPOLOGY_COMMENTS_MIDDLE,
        TOPOLOGY_COMMENTS_INTERSPERSED,
        TOPOLOGY_COMMENTS_END,
        TOPOLOGY_WHITESPACE_COMMENTS,
        TOPOLOGY_EMPTY_COMMENTS,
    ])
    def test_non_strict_mode_accepts_comments(self, topo_file):
        """Test that non-strict mode accepts and ignores all types of comments"""
        topo = topology.parse(topo_file, strict=False)
        assert len(topo.nodes) == 3
        assert len(topo.edges) == 2
        assert topo.nodes[0].label == "0_NodeA"
        assert topo.nodes[1].label == "1_NodeB"
        assert topo.nodes[2].label == "2_NodeC"

    def test_comments_preserve_data_accuracy(self):
        """Test that parsed data is identical whether comments are present or not"""
        topo_no_comments = topology.parse(TOPOLOGY_NO_COMMENTS, strict=False)
        topo_with_comments = topology.parse(TOPOLOGY_COMMENTS_INTERSPERSED, strict=False)

        assert topo_no_comments == topo_with_comments
        assert len(topo_no_comments.nodes) == len(topo_with_comments.nodes)
        assert len(topo_no_comments.edges) == len(topo_with_comments.edges)

    @pytest.mark.parametrize("topo_file", [
        TOPOLOGY_COMMENT_IN_HEADER,
        TOPOLOGY_COMMENT_IN_MEMO,
    ])
    def test_invalid_comments_fail_both_modes(self, topo_file):
        """Test that comments in headers/memos fail in both strict and non-strict modes"""
        with pytest.raises(errors.ParseError):
            topology.parse(topo_file, strict=True)
        with pytest.raises(errors.ParseError):
            topology.parse(topo_file, strict=False)

    def test_export_after_comment_parsing(self):
        """Test that export works correctly after parsing file with comments"""
        topo = topology.parse(TOPOLOGY_COMMENTS_INTERSPERSED, strict=False)

        # Export to string buffer
        from io import StringIO
        output = StringIO()
        topo.export(output)
        output_str = output.getvalue()

        # Verify export format
        lines = output_str.strip().split("\n")
        assert lines[0] == "NODES 3"
        assert lines[1] == "label x y"
        assert "EDGES 2" in lines
        assert "label src dest weight bw delay" in lines


class TestDemandsComments:
    def test_strict_mode_default(self):
        """Test that default behavior is strict=True"""
        with pytest.raises(errors.ParseError):
            demands.parse(DEMANDS_COMMENTS_START)

    def test_strict_mode_explicit_true(self):
        """Test that strict=True explicitly rejects comments"""
        with pytest.raises(errors.ParseError):
            demands.parse(DEMANDS_COMMENTS_START, strict=True)

    @pytest.mark.parametrize("demands_file", [
        DEMANDS_COMMENTS_START,
        DEMANDS_COMMENTS_INTERSPERSED,
        DEMANDS_COMMENTS_END,
        DEMANDS_WHITESPACE_COMMENTS,
    ])
    def test_strict_mode_rejects_all_comments(self, demands_file):
        """Test that strict mode rejects all types of comments"""
        with pytest.raises(errors.ParseError):
            demands.parse(demands_file, strict=True)

    @pytest.mark.parametrize("demands_file", [
        DEMANDS_COMMENTS_START,
        DEMANDS_COMMENTS_INTERSPERSED,
        DEMANDS_COMMENTS_END,
        DEMANDS_WHITESPACE_COMMENTS,
    ])
    def test_non_strict_mode_accepts_comments(self, demands_file):
        """Test that non-strict mode accepts and ignores all types of comments"""
        dems = demands.parse(demands_file, strict=False)
        assert len(dems.list) == 3
        assert dems.list[0].label == "demand_0"
        assert dems.list[1].label == "demand_1"
        assert dems.list[2].label == "demand_2"

    def test_comments_preserve_data_accuracy(self):
        """Test that parsed data is identical whether comments are present or not"""
        dems_no_comments = demands.parse(DEMANDS_NO_COMMENTS, strict=False)
        dems_with_comments = demands.parse(DEMANDS_COMMENTS_INTERSPERSED, strict=False)

        assert dems_no_comments == dems_with_comments
        assert len(dems_no_comments.list) == len(dems_with_comments.list)

    @pytest.mark.parametrize("demands_file", [
        DEMANDS_COMMENT_IN_HEADER,
        DEMANDS_COMMENT_IN_MEMO,
    ])
    def test_invalid_comments_fail_both_modes(self, demands_file):
        """Test that comments in headers/memos fail in both strict and non-strict modes"""
        with pytest.raises(errors.ParseError):
            demands.parse(demands_file, strict=True)
        with pytest.raises(errors.ParseError):
            demands.parse(demands_file, strict=False)

    def test_export_after_comment_parsing(self):
        """Test that export works correctly after parsing file with comments"""
        dems = demands.parse(DEMANDS_COMMENTS_INTERSPERSED, strict=False)

        # Export to string buffer
        from io import StringIO
        output = StringIO()
        dems.export(output)
        output_str = output.getvalue()

        # Verify export format
        lines = output_str.strip().split("\n")
        assert lines[0] == "DEMANDS 3"
        assert lines[1] == "label src dest bw"


class TestInstanceWithComments:
    def test_instance_with_commented_files_strict_mode(self):
        """Test that Instance creation fails with commented files in strict mode"""
        with pytest.raises(errors.ParseError):
            Instance(TOPOLOGY_COMMENTS_START, DEMANDS_COMMENTS_START, strict=True)

    def test_instance_with_commented_files_non_strict_mode(self):
        """Test that Instance creation works with commented files in non-strict mode"""
        instance = Instance(TOPOLOGY_COMMENTS_START, DEMANDS_COMMENTS_START, strict=False)
        assert len(instance.topology.nodes) == 3
        assert len(instance.topology.edges) == 2
        assert len(instance.demands.list) == 3
        assert instance.traffic_matrix.shape == (3, 3)

    def test_instance_validation_with_comments(self):
        """Test that validation works correctly when comments are present"""
        # This should work fine - the nodes in our test topology are 0, 1, 2
        # and the demands use these same node indices
        instance = Instance(TOPOLOGY_COMMENTS_START, DEMANDS_COMMENTS_START, strict=False)
        assert len(instance.topology.nodes) == 3
        assert len(instance.demands.list) == 3


class TestErrorReporting:
    def test_line_number_accuracy_with_skipped_comments(self):
        """Test that error line numbers are accurate when comments are skipped"""
        # Create a test file with comments and an error
        from io import StringIO

        # This will be tested once the implementation is complete
        pass

    def test_error_messages_in_non_strict_mode(self):
        """Test that error messages are still clear in non-strict mode"""
        # This will be tested once the implementation is complete
        pass
