"""
Main Orchestrator Entrypoint for NetMon-Report engine execution.
"""
from utils.data_generator import MockDataGenerator
from core.scanner import NetworkScanner
from core.analyzer import TrafficAnalyzer
from core.monitor import HealthMonitor
from reporting.csv_reporter import CSVReporter
from reporting.pdf_reporter import PDFExecutiveReporter
from config import RAW_DATA_DIR, REPORT_OUTPUT_DIR
from utils.logger import setup_logger

def main():
    logger = setup_logger("MainOrchestrator")
    logger.info("Initializing NetMon-Report Toolkit...")

    # Step 1: Bootstrap Synthetic Environment Datasets
    generator = MockDataGenerator()
    inventory_data = generator.generate_static_inventory()
    generator.generate_traffic_logs(records=150)
    generator.generate_performance_metrics(data_points=24)
    logger.info("Synthetic telemetry collection arrays bootstrapped cleanly.")

    # Step 2: Execute Network Profiling Scans
    scanner = NetworkScanner()
    profiled_hosts = scanner.ping_sweep_simulated(inventory_data)
    
    for host in profiled_hosts:
        if host["status"] == "Online":
            host["open_ports"] = scanner.scan_ports(host["ip"], [22, 80, 443, 445])

    # Step 3: Run In-depth Log Correlation Data Analysis
    analyzer = TrafficAnalyzer()
    analysis_results = analyzer.analyze_csv_logs(RAW_DATA_DIR / "traffic_logs.csv")

    # Step 4: System Resource Footprint Check
    monitor = HealthMonitor()
    system_health = monitor.collect_system_metrics()
    logger.info(f"Host Server Metrics -> CPU Usage: {system_health['cpu_utilization_pct']}%")

    # Step 5: Generate Structural Compliance CSV Reports
    csv_rep = CSVReporter()
    csv_rep.export_inventory(profiled_hosts, REPORT_OUTPUT_DIR / "discovered_assets.csv")

    # Step 6: Render Executable PDF Dashboard Report
    pdf_rep = PDFExecutiveReporter()
    pdf_rep.compile_document(
        scan_results=profiled_hosts,
        analysis=analysis_results,
        metrics_path=RAW_DATA_DIR / "performance_metrics.json",
        output_pdf_path=REPORT_OUTPUT_DIR / "Executive_Network_Security_Report.pdf"
    )

    logger.info("=== NETMON-REPORT TASK PIPELINE COMPLETE ===")
    logger.info(f"Review CSV outputs and generated PDF under: '{REPORT_OUTPUT_DIR.resolve()}'")

if __name__ == "__main__":
    main()