import yaml


class Dashboard:

    def __init__(self):
        super().__init__()
        self._load_configuration()

    def _load_configuration(self) -> None:
        config_yaml_stream = open('configs/dashboard.yaml', "r")
        self.leafs = yaml.load(config_yaml_stream)

    def register_entry(self, toggl_entry: dict) -> None:
        pass

    def generate_html(self) -> str:
        pass
