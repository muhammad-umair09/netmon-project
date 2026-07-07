"""
Synthetic Network Telemetry Generator.
Generates baseline distributions of hosts, logs, traffic statistics, and anomalies.
"""
import random
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from config import RAW_DATA_DIR

class MockDataGenerator:
    def __init__(self):
        self.mac_prefixes = ["00:50:56", "00:0C:29", "00:15:5D", "00:05:69"]
        self.host_templates = [
            {"ip": "192.168.1.1", "device": "Gateway Router", "os": "Cisco IOS"},
            {"ip": "192.168.1.10", "device": "Primary Domain Controller", "os": "Windows Server 2022"},
            {"ip": "192.168.1.20", "device": "Database Cluster Node 01", "os": "Ubuntu Server 22.04"},
            {"ip": "192.168.1.50", "device": "SecOps Workstation", "os": "Kali Linux"},
            {"ip": "192.168.1.101", "device": "Corporate Laptop", "os": "Windows 11"},
            {"ip": "192.168.1.102", "device": "Finance Desk Node", "os": "macOS Sequoia"},
            {"ip": "192.168.1.200", "device": "Unmanaged IoT Camera", "os": "Embedded Linux"}
        ]

    def _generate_mac(self) -> str:
        prefix = random.choice(self.mac_prefixes)
        suffix = ":".join(f"{random.randint(0, 255):02X}" for _ in range(3))
        return f"{prefix}:{suffix}"

    def generate_static_inventory(self) -> list:
        inventory = []
        for host in self.host_templates:
            inventory.append({
                "ip": host["ip"],
                "mac": self._generate_mac(),
                "hostname": host["device"],
                "os_guess": host["os"],
                "status": "Online" if host["ip"] != "192.168.1.200" else random.choice(["Online", "Offline"])
            })
        
        # Save inventory
        with open(RAW_DATA_DIR / "device_inventory.json", "w") as f:
            json.dump(inventory, f, indent=4)
        return inventory

    def generate_traffic_logs(self, records: int = 100):
        protocols = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS", "SSH", "SMB", "DNS"]
        file_path = RAW_DATA_DIR / "traffic_logs.csv"
        
        with open(file_path, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "src_ip", "src_port", "dst_ip", "dst_port", "protocol", "bytes_sent", "bytes_recv", "status"])
            
            base_time = datetime.now() - timedelta(hours=6)
            for i in range(records):
                timestamp = (base_time + timedelta(seconds=i * random.randint(10, 30))).strftime("%Y-%m-%d %H:%M:%S")
                src = random.choice(self.host_templates)["ip"]
                dst = random.choice(self.host_templates)["ip"]
                while dst == src:
                    dst = random.choice(self.host_templates)["ip"]
                
                proto = random.choice(protocols)
                sport = random.randint(1024, 65535)
                dport = random.choice([80, 443, 22, 53, 445]) if random.random() > 0.3 else random.randint(1024, 65535)
                
                bsent = random.randint(64, 1500) if proto != "HTTPS" else random.randint(1024, 500000)
                brecv = random.randint(64, 1500) if proto != "HTTPS" else random.randint(1024, 2000000)
                
                # Introduce anomalous event (potential data exfiltration)
                if i == records - 5:
                    src = "192.168.1.200"
                    dst = "203.0.113.50"  # External Rogue IP
                    proto = "HTTPS"
                    dport = 443
                    bsent = 45000000  # 45 MB exfil
                    brecv = 12000
                
                status = "Established" if proto in ["TCP", "HTTPS", "HTTP", "SSH"] else "Transmitted"
                if random.random() < 0.05 and i != records - 5:
                    status = "Failed"
                    
                writer.writerow([timestamp, src, sport, dst, dport, proto, bsent, brecv, status])

    def generate_performance_metrics(self, data_points: int = 24):
        file_path = RAW_DATA_DIR / "performance_metrics.json"
        metrics = []
        base_time = datetime.now() - timedelta(hours=data_points)
        
        for i in range(data_points):
            timestamp = (base_time + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S")
            metrics.append({
                "timestamp": timestamp,
                "network_utilization_pct": round(random.uniform(15.5, 92.4), 2),
                "avg_latency_ms": round(random.uniform(5.2, 42.1) if random.random() > 0.1 else random.uniform(120.0, 185.5), 2),
                "dropped_packets_pct": round(random.uniform(0.0, 1.5) if random.random() > 0.05 else random.uniform(3.5, 8.2), 3)
            })
            
        with open(file_path, "w") as f:
            json.dump(metrics, f, indent=4)