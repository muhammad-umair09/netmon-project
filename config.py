"""
Configuration Management Module for NetMon-Report.
Defines network subnets, targeting criteria, thresholds, and output paths.
"""
import os
from pathlib import Path

# Base Directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
REPORT_OUTPUT_DIR = DATA_DIR / "reports"

for folder in [RAW_DATA_DIR, REPORT_OUTPUT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Network Configurations
TARGET_SUBNET = "1192.168.1.0/24"  # Default fallback or simulated range
DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 443, 445, 3389, 8080]

# Threshold Constants for Alerts
LATENCY_CRITICAL_MS = 150.0
BANDWIDTH_WARNING_MBPS = 85.0
FAILED_CONN_THRESHOLD = 5

# Logging Config
LOG_FILE = BASE_DIR / "netmon.log"