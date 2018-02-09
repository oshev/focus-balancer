import yaml

from src import html_generator
from src.dashboard_node import DashboardNode, NodeType
from src.toggl import TogglEntry
from src.tools import get_week_start, get_day_start

FIELD_NAME = 'Leaf'
FIELD_LINK = 'Link'
FIELD_DAY_GOAL = 'DayGoal'
FIELD_WEEK_GOAL = 'WeekGoal'
FIELD_TITLE_REGEX = 'TitleRegex'
FIELD_TAGS = 'Tags'
FIELD_PARSED_LEAF = 'ParsedLeaf'

DASHBOARD_CONFIG_PATH = 'configs/dashboard.yaml'


class DashboardConfig:

    def __init__(self, dashboard_config_path=DASHBOARD_CONFIG_PATH):
        super().__init__()
        self.config_root = self._load_configuration(dashboard_config_path)
        self.tree_root = self._parse_config_node(self.config_root)  # keeps hierarchical structure
        self.tree_leafs_list = self.tree_root.sub_nodes_list()  # flatten, for faster checking the leafs

    @staticmethod
    def _load_configuration(dashboard_config_path) -> object:
        config_yaml_stream = open(dashboard_config_path, "r")
        return yaml.load(config_yaml_stream)

    @staticmethod
    def _get_field_or_none(leaf_dict: dict, field_name: str):
        return leaf_dict[field_name] if field_name in leaf_dict else None

    @staticmethod
    def _parse_tags(tags_field) -> list:
        if type(tags_field) == str:
            tag_groups = [tags_field]
        elif type(tags_field) == list:
            tag_groups = list(tags_field)
        else:
            tag_groups = []
        tag_sets = []
        for tag_group in tag_groups:
            tag_sets.append({tag.strip() for tag in tag_group.split(",")})
        return tag_sets if len(tag_sets) > 0 else None

    def _parse_config_node(self, config_node) -> DashboardNode:
        if type(config_node) == dict:
            dict_node = dict(config_node)
            name = self._get_field_or_none(dict_node, FIELD_NAME)
            if name is None and len(dict_node) == 1 and type(list(dict_node.values())[0]) == list:
                name = list(dict_node.keys())[0]
                children_config_nodes = list(list(dict_node.values())[0])
                children_parsed_nodes = []
                for node in children_config_nodes:
                    children_parsed_nodes.append(self._parse_config_node(node))
                return DashboardNode(node_type=NodeType.CATEGORY, name=name, children=children_parsed_nodes)
            else:
                link = self._get_field_or_none(dict_node, FIELD_LINK)
                day_goal = self._get_field_or_none(dict_node, FIELD_DAY_GOAL)
                week_goal = self._get_field_or_none(dict_node, FIELD_WEEK_GOAL)
                title_regex = self._get_field_or_none(dict_node, FIELD_TITLE_REGEX)
                tags = self._parse_tags(self._get_field_or_none(dict_node, FIELD_TAGS))
                return DashboardNode(node_type=NodeType.LEAF, name=name, link=link, day_goal=day_goal,
                                     week_goal=week_goal, title_regex=title_regex, tags=tags)

    def register_entry(self, toggl_entry: dict) -> None:
        week_start = get_week_start()
        day_start = get_day_start()
        for leaf in self.tree_leafs_list:
            entry = TogglEntry(toggl_entry)
            if leaf.match_title(entry.title) and leaf.match_tags(entry.tags):
                leaf.update_stats(entry.start_datetime,
                                  entry.stop_datetime,
                                  entry.duration,
                                  week_start, day_start)

    def generate_html(self) -> str:
        return html_generator.get_html(self.tree_root)
