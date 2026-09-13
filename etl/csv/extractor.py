from pathlib import Path

import pandas as pd


class CSVExtractor:
    def __init__(self, mode="upload"):
        self.mode = mode

    def extract(self, source):

        if self.mode == "upload":
            return self._extract_upload(source)

        elif self.mode == "path":
            return self._extract_path(source)

        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def _extract_upload(self, source):
        return pd.read_csv(source)

    def _extract_path(self, source):
        path = Path(source)

        if not path.is_file():
            print("File doesn't exist")
            return False

        print("File exists")
        return pd.read_csv(path)
