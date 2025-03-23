# Flight Insight
##### A Real-Time Flight Data Engineering Pipeline
Collect and display history of flight fares using the SkyScanner API

An **end-to-end data engineering project**.

---

### 🎯 Project Goal (High Level)
**Build a Data Pipeline to Collect, Store, Process, and Visualize Real-Time Flight Data**

You will:
- Use modern, production-ready tools
- Create a repeatable, automated data pipeline
- Include monitoring, testing, and documentation
- Deliver a mini dashboard or API

---



### 🔍 Use Case:
Collect global flight data (e.g. departures, arrivals, routes, delays), process it, and store it for trend analysis, alerts (like abnormal delays), or dashboards.

---

## 🧱 Tech Stack 

| Layer              | Tools/Tech                                      |
|-------------------|-------------------------------------------------|
| **Ingestion**      | Python, Requests, Airflow (Scheduler)           |
| **Orchestration**  | **Apache Airflow** (DAGs to automate ETL)       |
| **Storage**        | **PostgreSQL** (raw + cleaned data)             |
| **Processing**     | **dbt** (for SQL-based transformation)          |
| **Containerization**| **Docker** (run Airflow, PostgreSQL, etc.)     |
| **Monitoring**     | **Airflow UI**, **logging**, optional: Prometheus/Grafana |
| **Testing**        | Pytest + dbt tests                              |
| **Visualization**  | Streamlit or simple Flask dashboard             |
| **CI/CD (Bonus)**  | GitHub Actions                                  |
| **Infra (Bonus)**  | Terraform (if deploying on cloud)               |

---

## 🗂️ Project Structure
```
flight_insight/
├── dags/                   ← Airflow DAGs
├── data/                   ← Local storage (if any)
├── dbt/                    ← dbt models for transformation
├── scripts/                ← Custom Python scripts
│   └── extract_flight_data.py
├── docker/                 ← Docker configs
│   └── docker-compose.yml
├── airflow/                ← Airflow-specific config (plugins, etc.)
├── notebooks/              ← EDA, quick queries
├── tests/                  ← Unit and integration tests
├── README.md
├── requirements.txt
└── .env
```

---

## 📈 Possible Features
### 🔹 Basic MVP
- Connect to aviation-edge API (e.g., departures, delays)
- Store raw data in PostgreSQL
- Schedule ingestion daily/hourly using Airflow
- Transform data using dbt (normalize, calculate delay stats)
- Dashboard to view delay trends per airport

### 🔹 Advanced Add-Ons
- Deduplicate and validate using dbt tests
- Detect anomalies (e.g. delay spike) using a basic ML model or SQL rule
- Streamlit dashboard showing top delayed routes, airlines, etc.
- Alerts (Slack/email) on specific triggers (e.g. >3hr delay)
- Archive old data to S3 (mock or real)
- Expose cleaned data via REST API (Flask/FastAPI)

---

## ✅ This Project Shows Off:
- Modern ETL design (modular, scalable)
- Hands-on with orchestration (Airflow)
- Real-world data processing (messy API data)
- Writing clean, testable Python code
- Deployment and automation skills (Docker, Airflow)
- Data modeling and transformation (dbt)
- Optional: basic visualization (not just backend)

---

