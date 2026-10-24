# 🖥️ Automated Memory Monitoring & JIRA Incident Escalation Engine

[![CI Test Suite](https://github.com/AbdullahbinAmin/automated-memory-monitoring-jira-ticketing/actions/workflows/ci.yml/badge.svg)](https://github.com/AbdullahbinAmin/automated-memory-monitoring-jira-ticketing/actions)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![JIRA](https://img.shields.io/badge/Atlassian-JIRA_REST_API-0052CC?logo=jira&logoColor=white)
![Paramiko](https://img.shields.io/badge/Paramiko-SSH2_Automation-blue)
![Systemd](https://img.shields.io/badge/Linux-Systemd_Service-E95420?logo=ubuntu&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![SRE](https://img.shields.io/badge/SRE-Proactive_Monitoring-green)

> **Enterprise Site Reliability Engineering (SRE) Daemon**  
> *Proactively monitors Linux server memory pools over secure SSH, detects capacity threshold breaches, auto-creates high-priority Atlassian JIRA incidents, and dispatches managerial approval notifications via SMTP.*

---

## 📖 Overview

Memory exhaustion on critical Linux production nodes leads to kernel Out-Of-Memory (OOM) killer terminations, application crashes, and degraded user experiences.

This **SRE Incident Automation Engine** continuously monitors available memory across infrastructure nodes. When available memory falls below defined Service Level Objectives (SLOs):
1. **Automated Incident Creation**: Interacts with Atlassian JIRA Cloud/Server REST API to file a high-priority incident ticket under the designated operations project.
2. **Approval & Alert Dispatch**: Sends structured HTML notification emails via SMTP to team leads and stakeholder inboxes requesting immediate triage.
3. **Enterprise Hardening**: Runs as an isolated, non-root `systemd` daemon or containerized service with zero hardcoded credentials.

---

## 🏗️ Architecture & Escalation Flow

```mermaid
flowchart TD
    Daemon["⚙️ SRE Monitoring Daemon\n(automated-memory-monitoring)"] -->|Paramiko SSH: 'free -g'| RemoteServer["🐧 Production Linux Node\n(Target Infrastructure)"]
    
    RemoteServer -->|Parse Available RAM (GB)| Daemon
    
    Daemon --> Decision{"Available Memory\n<= Threshold?"}
    
    Decision -->|Yes: Breach Detected| JIRA["🎫 Atlassian JIRA REST API\nCreate High-Priority Issue"]
    Decision -->|No: Optimal State| Sleep["⏳ Log Optimal Status\nWait for Next Cycle"]
    
    JIRA --> Mail["📧 SMTP Mail Relay (TLS)\nDispatch Alert & Approval Request"]
    Mail --> OnCall["👨‍💻 SRE On-Call & Managerial Review"]
```

---

## ⚡ Quick Start

### 1. Prerequisites
- **Python**: 3.10 or higher
- **Network**: SSH network access to target Linux hosts (port 22)
- **Atlassian JIRA**: Account email and API token

### 2. Local Setup
```bash
# Clone the repository
git clone https://github.com/AbdullahbinAmin/automated-memory-monitoring-jira-ticketing.git
cd automated-memory-monitoring-jira-ticketing

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
```

### 3. Dry-Run Verification (No Live Credentials Required)
You can test the entire evaluation and alerting logic in simulation mode:

```bash
# Test optimal state (16 GB available - no incident created)
python automated-memory-monitoring-jira-ticketing.py --dry-run --mock-memory-gb 16

# Test critical breach state (0 GB available - triggers JIRA & Email simulation)
python automated-memory-monitoring-jira-ticketing.py --dry-run --mock-memory-gb 0
```

### 4. Run Automated Test Suite
```bash
python -m unittest discover tests
```

---

## ⚙️ Configuration Reference

All settings are configured securely via environment variables (or `.env` file):

| Variable | Description | Default |
| :--- | :--- | :--- |
| `MONITOR_SSH_HOST` | Target Linux host IP or FQDN | `127.0.0.1` |
| `MONITOR_SSH_USER` | SSH username | `ubuntu` |
| `MONITOR_SSH_PASSWORD` | SSH password (or use key path) | - |
| `MONITOR_SSH_KEY_PATH` | Path to private SSH key (`.pem` / `id_rsa`) | - |
| `MEMORY_THRESHOLD_GB` | Minimum acceptable available memory before alert | `1` |
| `JIRA_SERVER_URL` | Base Atlassian JIRA instance URL | `https://your-domain.atlassian.net` |
| `JIRA_USER_EMAIL` | JIRA user email | - |
| `JIRA_API_TOKEN` | JIRA REST API access token | - |
| `JIRA_PROJECT_KEY` | Target JIRA project key | `OPS` |
| `SMTP_SERVER` | Outgoing SMTP mail server | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port | `587` |
| `SMTP_USER` | SMTP authentication user | - |
| `ALERT_RECIPIENT_EMAIL`| SRE on-call / manager recipient email | - |

---

## 🚀 Production Deployment

### Option A: Linux Systemd Daemon
A hardened `systemd` service unit is provided in [`systemd/memory-monitor.service`](./systemd/memory-monitor.service):

```bash
# 1. Install project files to /opt/memory-monitor
sudo cp systemd/memory-monitor.service /etc/systemd/system/

# 2. Reload daemon and start service
sudo systemctl daemon-reload
sudo systemctl enable --now memory-monitor.service

# 3. Check logs
journalctl -u memory-monitor.service -f
```

### Option B: Docker Container
```bash
# Build the container image
docker build -t memory-monitor:latest .

# Run container with environment configuration
docker run -d --name memory-monitor --env-file .env memory-monitor:latest
```

---

## 🧪 Testing & CI Pipeline

Every push and pull request executes continuous integration tests under `.github/workflows/ci.yml`:
- Validates Python syntax and PEP8 standards.
- Executes automated unit tests with threshold breach assertions.

---

## 📄 License
This project is licensed under the MIT License.
