from pathlib import Path

class Space:
    def __init__(self, path: str | Path):
      self.path = Path(path)