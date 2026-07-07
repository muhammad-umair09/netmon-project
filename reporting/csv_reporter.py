"""
CSV Report Exporter Module.
Flattens hierarchical dataclasses into tabular CSV layouts.
"""
import csv
from pathlib import Path
from typing import List, Dict, Any
from utils.logger import setup_logger

class CSVReporter:
    def __init__(self):
        self.logger = setup_logger("CSVReporter")

    def export_inventory(self, data: List[Dict[str, Any]], target_path: Path):
        self.logger.info(f"Compiling inventory schema dataset to {target_path}...")
        if not data:
            return
        keys = data[0].keys()
        with open(target_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)