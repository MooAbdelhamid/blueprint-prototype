from etl.csv.extractor import CSVExtractor
from etl.csv.loader import CSVLoader
from etl.csv.transformer import CSVTransformer


class CSVPipeline:
    def __init__(self, manager):
        self.extractor = CSVExtractor()
        self.transformer = CSVTransformer()
        self.loader = CSVLoader()
        self.manager = manager

    def run(self, database, source):
        df = self.extractor.extract(source)
        df_out = self.transformer.transform(df)
        self.loader.load(self.manager, database, df_out)
