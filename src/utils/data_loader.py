import json
from pathlib import Path
from typing import Any


class DataLoader:
    """Utility class for loading data from JSON files"""

    def __init__(self, data_dir: str | Path):
        """Initialize DataLoader with directory containing JSON files"""
        if data_dir is None:
            raise ValueError("data_dir must be provided")

        self.data_dir = Path(data_dir)

        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self.data_dir}")

    def load_json(self, filename: str) -> Any:
        """
        Load data from JSON file

        Args:
            filename: Name of JSON file (with or without .json extension)

        Returns:
            Parsed JSON data

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
        """
        if not filename.endswith('.json'):
            filename = f"{filename}.json"

        file_path = self.data_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_products(self) -> list[dict]:
        """Load products from products.json"""
        return self.load_json('products.json')

    def load_customers(self) -> list[dict]:
        """Load customers from customers.json"""
        return self.load_json('customers.json')
