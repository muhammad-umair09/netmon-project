# NetMon-Report — Enterprise Network Monitoring & Security Reporting Framework

An automated, cross-platform Network Monitoring, Analytics, and Security Reporting Engine built in Python. Designed for Security Operations Center (SOC) analysts, Network Administrators, and blue-team practitioners looking to implement programmatic network visibility, asset tracking, log correlation, and compliance PDF generation.


## 📝 Overview

`NetMon-Report` replicates the functional mechanics of enterprise network monitoring solutions (like PRTG, SolarWinds, or Zeek logs) by abstracting and automating host discovery, connection status validation, traffic analysis, and alert notification triggers.

Asal duniya mein, ek SOC Analyst ya Network Engineer ka bohot saara waqt network par najar rakhne, threats dhoodhne, aur seniors ke liye reports banane mein jata hai. Yeh project dikhata hai ki kaise **Python scripting ke zariye in saare kaamo ko auto-pilot par dala ja sakta hai**.



## 🚀 Features

* **Asset Discovery & Inventory:** Programmatically sweeps subnets to track active hosts, log physical MAC addresses, and match device profiles.
* **Network Traffic Analytics:** Leverages highly efficient `pandas` data manipulation structures to parse raw flow logs, aggregate bandwidth metrics, and break down protocols.
* **Security Threat Detection:** Implements precise algorithmic heuristics to uncover anomalies such as massive horizontal data exfiltration spikes or brute-force/port scanning footprints.
* **Executive Document Compilation:** Uses `matplotlib` to render clean traffic distribution visuals and generates standardized, client-ready PDF compliance briefs via `fpdf2`.
* **Bare-Metal Resource Auditing:** Captures host environment baseline footprints (CPU, memory overhead, and network socket interface throughput).

## 🏗️ Architecture

The framework is decoupled into modular layers to maintain high code maintainability and test isolation:

1. **Bootstrap Layer (`utils/data_generator.py`)**: Populates the internal sandbox array with realistic network traffic signatures and anomaly datasets.
2. **Core Discovery and Scan Engine (`core/scanner.py`)**: Runs parallel network sweeping loops and tests common service ports.
3. **Data Core Analytics Layer (`core/analyzer.py`)**: Aggregates network trends and flags suspicious nodes.
4. **Export Engine (`reporting/`)**: Converts internal telemetry data arrays into clean CSV structures and visual PDF documents.


## 🛠️ Technology Stack

* **Programming Language:** Python 3.10+
* **Data Processing:** Pandas (Dataframe parsing & aggregation)
* **Visualization:** Matplotlib (Pie charts & volume trend arrays)
* **Document Engine:** FPDF2 (Strict coordinate-based PDF layout generation)
* **Hardware Instrumentation:** Psutil (Process & system instrumentation counters)


## 💾 Installation

### Prerequisites

* Ensure Python 3.10 or higher is installed on your workstation.
* Git command line tools.

### Clone Repository

```bash
git clone https://github.com/muhammad-umair09/netmon-project.git
cd netmon-report

```

### Install Dependencies

Create an isolated virtual environment and install the required dependencies:

```bash
# Initialize environment
python -m venv venv

# Activate environment (Linux/macOS)
source venv/bin/activate

# Activate environment (Windows)
.\venv\Scripts\activate

# Install required packages
pip install pandas matplotlib fpdf2 psutil

```

### Run Project

To bootstrap simulation events, profile devices, run security heuristics, and export reports, execute the master orchestrator pipeline script:

```bash
python main.py

```


## 📖 Usage

### Step-by-Step Pipeline Walkthrough

1. **System Initialization:** Running `main.py` creates a clean folder layout (`data/raw/` and `data/reports/`) to store the outputs.
2. **Traffic Generation:** The generator script populates `data/raw/traffic_logs.csv` with simulated network events. This includes standard traffic patterns along with a hidden high-volume exfiltration connection to an external address.
3. **Log Aggregation & Extraction:** The framework parses the logs to identify top active devices, classify communication protocols, and flag abnormal behaviors based on connection thresholds.
4. **Report Distribution:** The tool outputs a structured spreadsheet containing the discovered network devices (`discovered_assets.csv`) and creates a presentation-ready executive summary (`Executive_Network_Security_Report.pdf`).



## 📂 Project Structure

```text
netmon_project/
│
├── config.py                 # Core path configuration, subnet scopes, and threat alerts
├── main.py                   # Master engine orchestration entrypoint
├── netmon.log                # Production troubleshooting logs
│
├── core/                     # Structural Engine Functionality
│   ├── __init__.py
│   ├── analyzer.py           # Log analytics and threat detection heuristics
│   ├── monitor.py            # Local process resource monitoring
│   └── scanner.py            # Active asset scanning and device profiling
│
├── utils/                    # Shared Technical Utilities
│   ├── __init__.py
│   ├── data_generator.py     # Generates realistic network logs and attack traffic
│   └── logger.py             # Standardized logging facility (Console + File)
│
├── reporting/                # Formatting & Document Compilation
│   ├── __init__.py
│   ├── csv_reporter.py       # Outputs structured data to CSV formats
│   └── pdf_reporter.py       # Renders analytics dashboards and compiles PDFs
│
└── data/                     # Data Storage Layout
    ├── raw/                  # Ingested flow events and device logs
    └── reports/              # Final exported security briefs and spreadsheets

```


## ⚙️ Configuration

Global settings are managed in `config.py`. Update these parameters to match your target environment:

```python
# Network Configurations
TARGET_SUBNET = "192.168.1.0/24"  # Target subnet range for scanning
DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 443, 445, 3389, 8080]  # Ports evaluated by the scanner

# Threshold Constants for Alerts
LATENCY_CRITICAL_MS = 150.0       # Threshold for critical latency alerts
BANDWIDTH_WARNING_MBPS = 85.0     # Bandwidth usage warning threshold
FAILED_CONN_THRESHOLD = 5         # Failed connection threshold for scanning alerts

```



## 🔒 Security Considerations

* **Least Privilege:** This tool is designed to run in user-space using simulated telemetry datasets. If you switch to raw packet capture modes using native sockets or tools like Scapy, you must run the script with elevated administrative permissions (`sudo` or Windows Administrator mode).
* **Data Privacy:** Raw network logs can contain sensitive infrastructure details. In a production environment, ensure that all internal IP addresses, user credentials, and proprietary payload data are sanitized or masked before saving logs to public repositories.



## 🧪 Testing

The codebase features decoupled modules that make it easy to run automated unit tests. You can verify the data processing logic using standard Python testing tools:

```bash
# Run tests using standard unittest discovery
python -m unittest discover -s core -p "*_test.py"

```



## 📈 Performance Optimization

* **Data Aggregation Processing:** The system uses `pandas` vectorized operations instead of raw loops to parse logs, allowing it to efficiently process millions of raw connection events.
* **Low Memory Footprint:** The logging system streams text chunks directly to storage media rather than caching whole blocks in active system memory.

---

## 🗺️ Future Enhancements / Roadmap

* [ ] Add live packet capture functionality using non-blocking asynchronous socket architectures.
* [ ] Integrate native email notifications and webhook support for tools like Slack and Discord.
* [ ] Build a web-based dashboard interface using `Streamlit` to display network metrics in real time.
* [ ] Add support for export profiles that comply with industry standards like MITRE ATT&CK mapping frameworks.

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project Repository.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes with clear messages (`git commit -m 'Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a professional Pull Request for review.

---

## 🎨 Code Style Guidelines

The code in this repository follows standard formatting practices to ensure long-term readability:

* **PEP 8 Compliance:** All codebase modules use standard formatting conventions (4 spaces for indentation, clean variable naming).
* **Type Hinting:** Functions include type hints to ensure data integrity across the application pipeline.

---

## workflow Git Workflow

* Main development takes place on the `main` stable production branch.
* Use descriptive names for feature development branches (e.g., `feature/analytics-speedup` or `bugfix/pdf-render-clipping`).

---

