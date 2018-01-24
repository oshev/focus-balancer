from enum import Enum


class NodeType(Enum):
    CATEGORY = 1
    LEAF = 2


class DashboardNode:

    def __init__(self, node_type: NodeType, name: str=None, children: list=None, link: str=None,
                 day_goal: int=None, week_goal: int=None, title_regex: str=None, tags: list=None):
        self.node_type = node_type
        self.name = name
        if node_type == NodeType.LEAF:
            self.link = link
            self.day_goal = day_goal
            self.week_goal = week_goal
            self.title_regex = title_regex
            self.tag_sets = tags

            self.day_time = 0
            self.week_time = 0
            self.week_days = set()
            self.last_time = ""
        else:
            self.children = children

    def __repr__(self) -> str:
        if self.node_type == NodeType.LEAF:
            return "{}:{} ({}, {}, {}, {})".format(self.node_type, self.name, self.day_goal,
                                                   self.week_goal, self.title_regex, self.tag_sets)
        else:
            return "{}:{}, children={}".format(self.node_type, self.name, len(self.children))

    def sub_nodes_list(self) -> list:
        if self.node_type == NodeType.LEAF:
            return [self]
        else:
            result = []
            for child in list(self.children):
                result.extend(child.sub_nodes_list())
            return result
