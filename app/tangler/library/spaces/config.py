from pathlib import Path
from ..utils.file import YamlFile


class SpacesConfig(YamlFile):
    def __init__(self, config_path: str | Path):
        self.config: dict = {}

        def on_init(config):
            if config is None:
                raise ValueError("spaces config is missing or empty")
            self.config = config

        super().__init__(config_path, on_init=on_init)
