"""
PDF Compliance Executive Summary Generator.
Compiles analysis summaries into an executive-ready PDF report.
"""
import json
from pathlib import Path
from fpdf import FPDF
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils.logger import setup_logger

class PDFExecutiveReporter:
    def __init__(self):
        self.logger = setup_logger("PDFReporter")

    def generate_visual_dashboard(self, proto_data: dict, output_img_path: Path):
        """Generates the protocol distribution pie chart."""
        plt.figure(figsize=(6, 4))
        labels = list(proto_data.keys())
        sizes = list(proto_data.values())
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors[:len(labels)])
        plt.title("Network Protocol Traffic Mix Distribution", fontsize=12, fontweight='bold', pad=15)
        plt.tight_layout()
        plt.savefig(output_img_path, dpi=200)
        plt.close()

    def compile_document(self, scan_results: list, analysis: dict, metrics_path: Path, output_pdf_path: Path):
        self.logger.info("Initializing PDF generation pipeline...")
        img_dashboard = output_pdf_path.parent / "dashboard_temp.png"
        self.generate_visual_dashboard(analysis["protocol_distribution"], img_dashboard)
        
        pdf = FPDF()
        pdf.add_page()
        
        # Title Block
        pdf.set_fill_color(31, 58, 86) # Deep Navy
        pdf.rect(0, 0, 210, 38, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 10, "NETMON-REPORT: EXECUTIVE SECURITY BRIEF", ln=True, align='C')
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 5, f"Automated Network Monitoring & Security Audit Logs", ln=True, align='C')
        pdf.ln(15)
        
        # Section: Metadata Summary
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "1. Executive Operational Assessment", ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 5, f"Total Ingested Log Telemetry Flows: {analysis['total_records']} events\n"
                            f"Aggregated Network Traffic Volume: {analysis['total_volume_gb']} GB\n"
                            f"Total Devices Tracked in Subnet Inventory: {len(scan_results)} hosts")
        pdf.ln(5)
        
        # Section: Alerts Block
        pdf.set_fill_color(248, 215, 218) # Soft Red Alert Background
        pdf.set_text_color(114, 28, 36)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, " Security Operational Alerts Identified:", ln=True, fill=True)
        pdf.set_font("Arial", '', 9)
        for alert in analysis["alerts"]:
            pdf.multi_cell(0, 5, f" -> [{alert['severity']}] Node: {alert['source']} - {alert['message']}", fill=True)
        pdf.ln(5)
        
        # Section: Data Chart
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "2. Protocol Decomposition Dashboard", ln=True)
        pdf.image(str(img_dashboard), x=15, w=130)
        pdf.ln(5)

        # Section: Device Inventory Table
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "3. Managed Asset Inventory Profile", ln=True)
        pdf.set_font("Arial", 'B', 10)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(40, 7, "IP Address", 1, 0, 'C', True)
        pdf.cell(45, 7, "MAC Signature", 1, 0, 'C', True)
        pdf.cell(60, 7, "Identified Asset Name", 1, 0, 'C', True)
        pdf.cell(30, 7, "Operational State", 1, 1, 'C', True)
        
        pdf.set_font("Arial", '', 9)
        for host in scan_results:
            pdf.cell(40, 6, host["ip"], 1, 0, 'C')
            pdf.cell(45, 6, host["mac"], 1, 0, 'C')
            pdf.cell(60, 6, host["hostname"], 1, 0, 'L')
            pdf.cell(30, 6, host["status"], 1, 1, 'C')

        # Output file write
        pdf.output(str(output_pdf_path))
        self.logger.info(f"PDF Successfully rendered and compiled: {output_pdf_path}")
        if img_dashboard.exists():
            img_dashboard.unlink()