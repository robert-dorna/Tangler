from pathlib import Path
from .library.spaces.config import SpacesConfig


class Tangler:
    def __init__(self, spaces_config: str | Path | SpacesConfig):
        if not isinstance(spaces_config, SpacesConfig):
            spaces_config = SpacesConfig(spaces_config)

        self.spaces_config = spaces_config

    def run(self, argv: list) -> None:
        # TODO: use some library to parse command line

        if len(argv) < 2 or argv[1] not in ["server", "cli"]:
            raise ValueError("usage: tangler <cli|server> [...cli params]")

        if argv[1] == "server":
            from .server import Server

            server = Server(spaces_config=self.spaces_config)
            server.run()

        else:
            from .cli import Cli

            cli = Cli(spaces_config=self.spaces_config)
            cli.run(argv[2:])
