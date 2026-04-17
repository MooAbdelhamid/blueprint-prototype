"""
Base Transformer Interface
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class BaseTransformer(ABC):
    """
    Base class for all transformers
    """

    def __init__(self, source_id: str):
        self.source_id = source_id

    def transform(self, records: List[Dict]) -> List[Dict]:
        """
        Main entry point for transformation pipeline
        """

        if not records:
            return []

        records = self._normalize_columns(records)
        records = self._clean(records)
        records = self._map_schema(records)
        records = self._add_metadata(records)

        return records

    @abstractmethod
    def __normalize_columns(self, records: List[Dict]) -> List[Dict]:
        """Rename columns to a consistent format"""
        pass

    @abstractmethod
    def __clean(self, records: List[Dict]) -> List[Dict]:
        """Handle nulls, types, trimming, etc."""
        pass

    @abstractmethod
    def _map_schema(self, records: List[Dict]) -> List[Dict]:
        """Map source fields to internal schema"""
        pass

    @abstractmethod
    def _add_metadata(self, records: List[Dict]) -> List[Dict]:
        """Map source fields to internal schema"""
        pass
