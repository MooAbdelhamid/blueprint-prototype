"""
Base Connector Interface
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class SourceType(Enum):
    """Types of data sources supported"""

    CSV = "csv"
    NOONCSV = "noon_csv"
    AMAZONCSV = "amazon_csv"


class ConnectionStatus(Enum):
    """Status of a connector's connection"""

    NOT_CONNECTED = "not_connected"
    CONNECTED = "connected"
    FAILED = "failed"
    AUTHENTICATING = "authenticating"


class BaseConnector(ABC):
    """
    Base class that all data source connectors must inherit from
    """

    def __init__(self, source_id: str, config: Dict):
        """
        Args:
            source_id: unique identifier for the data source
            config: Configuration dict
        """
        self.source_id = source_id
        self.config = config
        self.status = ConnectionStatus.NOT_CONNECTED

    @abstractmethod
    def authenticate(self) -> bool:
        """
        Establish connection to the data source

        Returns:
            True if authentication successful, False otherwise
        """
        pass

    @abstractmethod
    def test_connection(self) -> Dict:
        """
        Test if the connection is working

        Returns:
            Dict with status and any error message
            Example: {'success': True, 'message': 'Connected to Shopify'}
        """
        pass

    @abstractmethod
    def extract_customers(self, since: Optional[datetime] = None) -> List[Dict]:
        """
        Extract customer data from the source


        Args:
            since: Only get records created/updated after this datetime (optional)

        Returns:
            List of dictionaries, each representing a customer in the SOURCE format
            Example: [{'id': '123', 'email': 'test@test.com', ...}, ...]
        """
        pass

    @abstractmethod
    def extract_products(self, since: Optional[datetime] = None) -> List[Dict]:
        """
        Extract product data from the source.

        Returns:
            List of dictionaries in SOURCE format
        """
        pass

    @abstractmethod
    def extract_orders(self, since: Optional[datetime] = None) -> List[Dict]:
        """
        Extract order data from the source.

        Returns:
            List of dictionaries in SOURCE format
        """
        pass

    def get_source_type(self) -> SourceType:
        """
        Get the type of this data source.

        Returns:
            SourceType enum value
        """
        return SourceType.CSV  # Override in subclasses

    def get_sync_status(self) -> Dict:
        """
        Get current status of this connector.

        Returns:
            Dict with connection status and metadata
        """
        return {
            "source_id": self.source_id,
            "status": self.status.value,
            "source_type": self.get_source_type().value,
        }
