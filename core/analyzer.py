"""
Threat Analysis Engine.
Analyzes volumetric telemetry trends and flag anomalous events.
"""
import pandas as pd
from typing import List, Dict, Any
from utils.logger import setup_logger
from config import BANDWIDTH_WARNING_MBPS, FAILED_CONN_THRESHOLD

class TrafficAnalyzer:
    def __init__(self):
        self.logger = setup_logger("AnalyzerEngine")

    def analyze_csv_logs(self, csv_path: str) -> Dict[str, Any]:
        """Processes logs using Pandas dataframes to calculate security metrics."""
        self.logger.info(f"Ingesting raw network flow records from {csv_path}...")
        df = pd.read_csv(csv_path)
        
        total_bytes = df['bytes_sent'].sum() + df['bytes_recv'].sum()
        protocol_counts = df['protocol'].value_counts().to_dict()
        
        # Identify top talkers
        top_talkers = df.groupby('src_ip')['bytes_sent'].sum().nlargest(3).to_dict()
        
        # Check failed connections (Suspicious Scan Behaviors)
        failed_conns = df[df['status'] == 'Failed']
        failed_counts = failed_conns.groupby('src_ip').size().to_dict()
        
        alerts = []
        for ip, count in failed_counts.items():
            if count >= FAILED_CONN_THRESHOLD:
                alerts.append({
                    "severity": "MEDIUM",
                    "source": ip,
                    "message": f"Potential port-scanning/brute-force anomaly detection. {count} failed sessions."
                })
                
        # Check for exfiltration spike
        large_uploads = df[df['bytes_sent'] > 10000000] # > 10MB
        for _, row in large_uploads.iterrows():
            alerts.append({
                "severity": "HIGH",
                "source": row['src_ip'],
                "message": f"Data exfiltration warning: {row['bytes_sent'] / (1024*1024):.2f} MB uploaded to external host {row['dst_ip']} via {row['protocol']}."
            })
            
        return {
            "total_records": len(df),
            "total_volume_gb": round(total_bytes / (1024**3), 4),
            "protocol_distribution": protocol_counts,
            "top_talkers": top_talkers,
            "alerts": alerts
        }