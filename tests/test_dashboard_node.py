from src.dashboard_node import DashboardNode, NodeType


class TestDashboardNode:

    def test_match_title_simple(self):
        node = DashboardNode(NodeType.LEAF, title_regex="Morning writing")
        assert node.match_title("Morning writing")

    def test_match_title_pattern(self):
        node = DashboardNode(NodeType.LEAF, title_regex="Morning.*")
        assert node.match_title("Morning writing")

    def test_match_tags_empty(self):
        node = DashboardNode(NodeType.LEAF, tags=[])
        assert node.match_tags(["english", "exercise", "writing"]) is not True

    def test_update_stats(self):
        # TODO
        pass

    def test_sub_nodes_list(self):
        # TODO
        pass
