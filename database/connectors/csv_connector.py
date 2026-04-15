"""
CSV Connector - Reads data from csv file
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import ClassVar, Dict, List, Optional

import pandas as pd
from base_connector import BaseConnector, ConnectionStatus, SourceType

logger = logging.getLogger(__name__)


class CSVConnector(BaseConnector):
    """
    Connector for reading data from CSV files.
    """

    SCHEMAS: ClassVar[Dict] = {
        "orders": {
            "required": ["order_id", "customer_id"],
            "optional": ["total", "currency"],
        },
        "customers": {
            "required": ["customer_id", "email"],
            "optional": ["name", "phone"],
        },
        "products": {
            "required": ["product_id", "name"],
            "optional": ["price", "category"],
        },
    }

    def __init__(self, source_id: str, config: Dict):
        """
        Initialize CSV connector.

        Args:
            ource_id: Unique ID for this data source
            config: Configuration dictionary with keys:
                - file_path: Path to the CSV file
                - delimiter: CSV delimiter (default: ',')
                - encoding: File encoding (default: 'utf-8')
        """
        super().__init__(source_id, config)

        self.file_path = Path(config.get("file_path"))
        self.delimiter = config.get("delimiter", ",")
        self.encoding = config.get("encoding", "utf-8")

        self.data = None
        self._row_count = 0

    def get_source_type(self) -> SourceType:
        """Override base method to return CSV type"""
        return SourceType.CSV

    def authenticate(self) -> bool:
        """
        For CSV files, authentication means checking the file exists and readable

        Returns:
            True if file exists and readable
        """
        try:
            if not self.file_path.exists():
                logger.error(f"CSV file not found: {self.file_path}")
                self.status = ConnectionStatus.FAILED
                return False

            if not self.file_path.is_file():
                logger.error(f"Path is not a file: {self.file_path}")
                self.status = ConnectionStatus.FAILED
                return False

            pd.read_csv(
                self.file_path,
                nrows=5,
                delimiter=self.delimiter,
                encoding=self.encoding,
            )

            self.status = ConnectionStatus.CONNECTED
            logger.info(f"CSV file validated: {self.file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to validate CSV file: {e}")
            self.status = ConnectionStatus.FAILED
            return False

    def test_connection(self) -> Dict:
        """
        Test the CSV file connection

        Returns:
            Status dictionary
        """
        is_valid = self.authenticate()

        if is_valid:
            # Get metadata about the file
            try:
                df = pd.read_csv(
                    self.file_path,
                    nrows=0,
                    delimiter=self.delimiter,
                    encoding=self.encoding,
                )

                return {
                    "success": True,
                    "message": "Successfully connected to CSV file",
                    "metadata": {
                        "file_path": str(self.file_path),
                        "columns": list(df.columns),
                    },
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"File exists but cannot read: {str(e)}",
                }
        else:
            return {
                "success": False,
                "message": f"CSV file not found or not readable: {self.file_path}",
            }

    def _read_csv(self) -> pd.DataFrame:
        """
        Internal method to read CSV file

        Returns:
            Pandas DataFrame with all rows
        """

        if self.data is None:
            logger.info(f"Reading CSV file: {self.file_path}")

            self.data = pd.read_csv(
                self.file_path,
                delimiter=self.delimiter,
                encoding=self.encoding,
                na_values=["", "NULL", "null", "N/A", "n/a", "NA"],
                keep_default_na=True,
            )

            self._row_count = len(self.data)
            logger.info(
                f"CSV loaded: {self._row_count} rows, {len(self.data.columns)} columns"
            )

        return self.data

    def _dataframe_to_dict_list(self, df: pd.DataFrame) -> List[Dict]:
        """
        Converts pandas DataFrame to list of dictionaries

        Args:
            df: Panda DataFrame

        Returns:
            List of dictionaries
        """
        df_clean = df.where(pd.notnull(df), None)

        records = df_clean.to_dict(orient="records")

        return records

    def _extract_entity(self, entity: str) -> List[Dict]:
        """
        Generic extraction function

        Args:
            entity: Entity to extract from file

        Returns:
            List of dictionaries
        """
        try:
            df = self._read_csv()
            schema = self.SCHEMAS[entity]

            required = schema["required"]
            optional = schema["optional"]

            missing = [c for c in required if c not in df.columns]

            if missing:
                logger.warning(
                    f"Skipping {entity}. Missing required columns: {missing}"
                )
                return []

            available_optional = [c for c in optional if c in df.columns]

            selected_cols = required + available_optional

            df_entity = df[selected_cols]

            return self._dataframe_to_dict_list(df_entity)

        except Exception as e:
            logger.error(f"Failed to extract {entity}: {e}")
            return []

    def extract_customers(self, since: Optional[datetime] = None) -> List[Dict]:
        """Extract customers data from CSV"""
        return self._extract_entity("customers")

    def extract_products(self, since: Optional[datetime] = None) -> List[Dict]:
        """Extract products data from CSV"""
        return self._extract_entity("products")

    def extract_orders(self, since: Optional[datetime] = None) -> List[Dict]:
        """Extract orders data from CSV"""
        return self._extract_entity("orders")
