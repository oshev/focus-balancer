from enum import Enum
import re


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
            self.last_time = None
        else:
            self.children = children

    def __repr__(self) -> str:
        if self.node_type == NodeType.LEAF:
            return "{}:{} ({}, {}, {}, {})".format(self.node_type, self.name, self.day_goal,
                                                   self.week_goal, self.title_regex, self.tag_sets)
        else:
            return "{}:{}, children={}".format(self.node_type, self.name, len(self.children))

    def update_stats(self, start, stop, seconds, week_start, day_start):
        if start > week_start:
            self.week_time += seconds
            self.week_days.add(start.weekday())
        if start > day_start:
            self.day_time += seconds
        if self.last_time is None or stop > self.last_time:
            self.last_time = stop

    def sub_nodes_list(self) -> list:
        if self.node_type == NodeType.LEAF:
            return [self]
        else:
            result = []
            for child in list(self.children):
                result.extend(child.sub_nodes_list())
            return result

    def match_title(self, title: str) -> bool:
        if self.title_regex is None:
            return True
        return re.match(self.title_regex, title) is not None

    def match_tags(self, tags_list):
        if self.tag_sets is None or tags_list is None:
            return True
        input_tags_set = set(tags_list)
        for tags_set in self.tag_sets:
            if tags_set.issubset(input_tags_set):
                return True
        return False
