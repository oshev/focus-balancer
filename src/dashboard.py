import yaml

FIELD_NAME = 'Leaf'
FIELD_LINK = 'Link'
FIELD_DAY_GOAL = 'DayGoal'
FIELD_WEEK_GOAL = 'WeekGoal'
FIELD_TITLE_REGEX = 'TitleRegex'
FIELD_TAGS = 'Tags'
FIELD_PARSED_LEAF = 'ParsedLeaf'


DASHBOARD_CONFIG_PATH = 'configs/dashboard.yaml'


class DashboardLeaf:

    def __init__(self, leaf_dict: dict):
        self.name = self._get_field_or_none(leaf_dict, FIELD_NAME)
        self.link = self._get_field_or_none(leaf_dict, FIELD_LINK)
        self.day_goal = self._get_field_or_none(leaf_dict, FIELD_DAY_GOAL)
        self.week_goal = self._get_field_or_none(leaf_dict, FIELD_WEEK_GOAL)
        self.title_regex = self._get_field_or_none(leaf_dict, FIELD_TITLE_REGEX)
        if FIELD_TAGS in leaf_dict:  # create a list of sets of tags
            if type(leaf_dict[FIELD_TAGS]) == str:
                tag_groups = [leaf_dict[FIELD_TAGS]]
            elif type(leaf_dict[FIELD_TAGS]) == list:
                tag_groups = list(leaf_dict[FIELD_TAGS])
            else:
                tag_groups = []
            self.tag_sets = []
            for tag_group in tag_groups:
                self.tag_sets.append({tag.strip() for tag in tag_group.split(",")})
        else:
            self.tag_sets = None

        self.day_time = 0
        self.week_time = 0
        self.week_days = set()
        self.last_time = ""

    @staticmethod
    def _get_field_or_none(leaf_dict: dict, field_name: str):
        return leaf_dict[field_name] if field_name in leaf_dict else None


class Dashboard:

    def __init__(self, dashboard_config_path=DASHBOARD_CONFIG_PATH):
        super().__init__()
        self._load_configuration(dashboard_config_path)

    @staticmethod
    def _extend_with_parsed_leaves(node) -> None:
        if type(node) == dict:
            dict_node = dict(node)
            if FIELD_NAME in dict_node:
                dict_node[FIELD_PARSED_LEAF] = DashboardLeaf(node)
            else:
                for child_node in dict_node.values():
                    Dashboard._extend_with_parsed_leaves(child_node)
        elif type(node) == list:
            list_node = list(node)
            for child_node in list_node:
                Dashboard._extend_with_parsed_leaves(child_node)

    def _load_configuration(self, dashboard_config_path) -> None:
        config_yaml_stream = open(dashboard_config_path, "r")
        self.root = yaml.load(config_yaml_stream)
        self._extend_with_parsed_leaves(self.root)

    def register_entry(self, toggl_entry: dict) -> None:
        pass

    def generate_html(self) -> str:
        pass
