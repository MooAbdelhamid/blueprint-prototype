from pathlib import Path

import pandas as pd


class CSVExtractor:
    def extract(self, path):
        path = Path(path)

        if not path.is_file():
            print("File doesn't exist")
            return False

        print("File exists")
        return pd.read_csv(path)
