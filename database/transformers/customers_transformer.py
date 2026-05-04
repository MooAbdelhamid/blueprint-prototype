from typing import Dict, List

from database.transformers.base_transformer import BaseTransformer


class CustomersTransformer(BaseTransformer):
    def __init__(self, source_id: str):
        """
        Pass
        """
        super().__init__(source_id)

        self.data = None
        self._row_count = 0

    def __clean(self, records: List[Dict]) -> List[Dict]:
        return records

    def _map_schema(self, records: List[Dict]) -> List[Dict]:
        rename_map = {"customer_id": "customer_id", "email": "email", "name": "name"}
        data = [{rename_map.get(k, k): v for k, v in row.items()} for row in records]
        return data
