"""
System and Environment Health Monitor.
Measures local bandwidth and resource allocation footprints.
"""
import psutil
from datetime import datetime
from utils.logger import setup_logger

class HealthMonitor:
    def __init__(self):
        self.logger = setup_logger("HealthMonitor")

    def collect_system_metrics(self) -> dict:
        """Captures hardware resources and basic network IO counters."""
        self.logger.info("Gathering engine baseline environment usage...")
        net_io = psutil.net_io_counters()
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu_utilization_pct": psutil.cpu_percent(interval=0.1),
            "memory_utilization_pct": psutil.virtual_memory().percent,
            "bytes_sent_total": net_io.bytes_sent,
            "bytes_recv_total": net_io.bytes_recv
        }