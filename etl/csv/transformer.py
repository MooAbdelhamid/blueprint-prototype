import uuid

import pandas as pd


class CSVTransformer:
    SOURCE_COLUMNS = {
        "order_date": "Day",
        "total_value": "Total sales",
    }

    def transform(self, df):
        # Verify every expected source column exists
        missing_columns = [
            source_col
            for source_col in self.SOURCE_COLUMNS.values()
            if source_col not in df.columns
        ]

        if missing_columns:
            print(f"Missing columns are {missing_columns}")
            return False

        # Create output using an explicit source -> destination mapping
        dict_out = {
            output_col: df[source_col]
            for output_col, source_col in self.SOURCE_COLUMNS.items()
        }

        df_out = pd.DataFrame(dict_out)

        df_out["order_date"] = pd.to_datetime(df_out["order_date"])

        # Generate a UUID for each output column
        df_out["order_id"] = [str(uuid.uuid4()) for _ in range(len(df_out))]

        return df_out
