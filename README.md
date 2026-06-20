
# Real-Time Banking Transaction Intelligence Platform

> An end-to-end, production-style data platform combining real-time streaming ingestion, lakehouse architecture, machine learning, and an agentic AI investigation interface — processing **5.3M+ synthetic banking transactions** to demonstrate transaction monitoring, fraud detection, risk scoring, and AI-augmented analyst workflows.

**Master's Capstone Project** · Wilfrid Laurier University, Master of Applied Computing
**Co-built by:** Faisal Ul Haque Mohammed and Darshil K Shah
**Completed:** April 2026

---

## 📐 Architecture Overview

The platform follows a **medallion lakehouse architecture** with the following layers:

| Layer | Purpose | Technologies |
|-------|---------|--------------|
| **Ingestion** | Real-time transaction event capture | Apache Kafka (Confluent 7.5.0) |
| **Processing** | Distributed streaming + batch transformations | Apache Spark 3.5.1 (Core, SQL, Structured Streaming) |
| **Catalog** | Hive-ecosystem table catalog | Apache Hive Metastore 4.0.0 + HiveServer2 (Postgres-backed) |
| **Storage** | Bronze / Silver / Gold lakehouse tables | Apache Iceberg on Azure Blob Storage (ADLS Gen2) |
| **Orchestration** | DAG-based workflow scheduling with branching logic | Apache Airflow 2.9.3 (25-task DAG, retraining gates) |
| **Serving** | Curated analytical store + dashboards | Azure SQL Database, Snowflake, Tableau |
| **ML Lifecycle** | Training, registry, monitoring, promotion automation | Scikit-learn, XGBoost, custom MLOps framework |
| **Agentic AI** | NLP-driven analyst investigation interface | LangChain + Ollama (llama3.1:8b) + ChromaDB + Flask |

---

## ✨ Key Capabilities

### 🌊 Real-Time Streaming Pipeline
- Kafka topics ingest synthetic transaction events with configurable throughput.
- Spark Structured Streaming consumes events into the Bronze layer with watermarking and stateful windowed aggregations.
- Dual-version producer/consumer patterns for backwards compatibility.

### 🏛️ Lakehouse Storage (Apache Iceberg)
- **Bronze:** Raw event capture with full lineage
- **Silver:** Cleaned, validated, deduplicated transactions
- **Gold:** Business-ready aggregates and ML feature stores
- `MERGE INTO` upserts for **idempotent, restart-safe** loads
- Schema evolution and time travel for historical analysis

### 🗂️ Hadoop-Ecosystem Catalog
- Apache Hive Metastore (Hive 4.0.0) backed by PostgreSQL
- HiveServer2 for Thrift-based SQL access on port 10000
- Iceberg tables registered against Hive Metastore — compatible with Spark SQL, Trino, and standard BI tools

### 🤖 Machine Learning Portfolio
- **Customer Segmentation:** KMeans + PCA with silhouette-based K selection
- **Anomaly Detection Ensemble:** Isolation Forest + LOF + One-Class SVM with majority voting and percentile scoring (the foundational ML methodology behind modern AML transaction-monitoring systems)
- **Fraud Classification Ensemble:** Logistic Regression, Random Forest, Gradient Boosting, XGBoost — evaluated on precision / recall / F1 / ROC-AUC / PR-AUC
- **Spend Prediction:** Random Forest Regressor with leakage-safe feature engineering

### 🔁 MLOps Lifecycle
- JSON-based **versioned model registry** with semantic versioning
- Automated **promotion gates** (R² and metric-threshold comparison)
- **Run-history tracking** and monitoring with metric drift detection
- **Automated retraining decisions** via Airflow branching (`sys.exit(1)` triggers retraining gates within the 25-task DAG)
- Auto-archiving of superseded model versions

### 🧠 Agentic AI Investigation Interface
A Flask-based service that lets analysts query the platform in natural language:

- **LangChain semantic intent routing** across seven domain tools (KPI, risk, anomaly, segmentation, spend prediction, streaming, investigation)
- **Ollama (llama3.1:8b)** as the local LLM backbone — no external API dependencies
- **ChromaDB** vector store for retrieval-augmented context
- **Four-step routing pipeline:**
  1. Follow-up question detection
  2. Semantic intent classification
  3. Keyword fallback
  4. LLM context augmentation
- **Anti-hallucination guardrails** — the model is constrained to retrieved structured outputs and forbidden from inventing metrics, IDs, dates, or model outputs.

### 📊 Business Intelligence
- Executive dashboard (Tableau)
- Real-time monitoring dashboard
- Geographic distribution dashboard

---

## 🧱 Tech Stack

| Category | Technologies |
|----------|--------------|
| **Languages** | Python 3.11, SQL, Bash |
| **Streaming** | Apache Kafka 7.5.0 (Confluent), Apache Spark 3.5.1 (Structured Streaming) |
| **Storage & Catalog** | Apache Iceberg, Apache Hive Metastore 4.0.0, HiveServer2, Azure Blob Storage (ADLS Gen2), PostgreSQL 15 |
| **Orchestration** | Apache Airflow 2.9.3 (LocalExecutor) |
| **Serving** | Azure SQL Database, Snowflake, Tableau |
| **ML / Data Science** | Scikit-learn, XGBoost, Pandas, NumPy |
| **Generative AI** | LangChain, Ollama (llama3.1:8b), ChromaDB, Flask |
| **DevOps** | Docker, Docker Compose, Git, Linux |

---

## 📂 Project Structure

```
.
├── producer/                 # Kafka transaction producer (dual-version)
├── consumer/                 # Streaming & batch Spark consumers
├── airflow_docker/           # Airflow + Spark + Kafka + Hive docker-compose stack
│   ├── dags/                 # Airflow DAGs (25-task pipeline)
│   ├── spark/                # Spark configuration
│   └── jars/                 # JDBC drivers (PostgreSQL, etc.)
├── cloud/                    # Azure integration scripts
├── ml/                       # Model training, evaluation, registry
│   ├── train_models.py       # End-to-end training entrypoint
│   ├── registry/             # Versioned model artifacts
│   └── monitoring/           # Drift detection and metric tracking
├── agentic_ai/               # LangChain + Ollama + Flask service
│   ├── app.py                # Flask REST API entrypoint
│   ├── tools/                # Seven domain tools
│   └── routing/              # Multi-stage routing logic
├── bi_exports/               # BI-ready outputs (Parquet / CSV)
├── tableau/                  # Dashboards and screenshots
├── dataset/                  # Dataset reference and sample
├── docs/                     # Architecture diagrams and reports
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- **Docker** and **Docker Compose**
- **Python 3.11+**
- **Ollama** (for local LLM runtime) — [install guide](https://ollama.com/)
- Azure account with Blob Storage and SQL Database *(optional — local-only mode supported)*

### 1. Clone the repository

```bash
git clone https://github.com/faisalhaq02/Real-Time-Banking-Transaction-Intelligence-Platform-Using-Streaming-and-Lakehouse-Architecture.git
cd Real-Time-Banking-Transaction-Intelligence-Platform-Using-Streaming-and-Lakehouse-Architecture
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
AIRFLOW_UID=50000

# Azure
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
BI_CONTAINER_NAME=bi-exports
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=banking_intelligence_db
AZURE_SQL_USERNAME=your_username
AZURE_SQL_PASSWORD=your_password
AZURE_SQL_ODBC_DRIVER=ODBC Driver 18 for SQL Server

# Kafka
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

> ⚠️ `.env` is excluded from version control. Replace placeholders with your own credentials.

### 3. Set up Python environment

```bash
python3 -m venv airflow_venv
source airflow_venv/bin/activate
pip install -r requirements.txt
```

### 4. Bring up the stack

```bash
cd airflow_docker
docker compose up -d
```

This starts: PostgreSQL (Airflow + Hive metastores), Airflow webserver + scheduler, Spark master + worker, Hive Metastore, HiveServer2, Zookeeper, and Kafka.

### 5. Access services

| Service | URL |
|---------|-----|
| Airflow UI | http://localhost:8082 |
| Spark Master UI | http://localhost:8081 |
| HiveServer2 (Thrift) | localhost:10000 |
| Kafka | localhost:9092 |
| Flask API (agentic AI) | http://localhost:5000 *(after step 9)* |

### 6. Run the producer

```bash
python producer/transaction_producer_v2.py
```

### 7. Run the streaming consumer

```bash
python consumer/consumer_file.py
```

### 8. Trigger the Airflow DAG

Open the Airflow UI and manually trigger the main pipeline DAG. The 25-task DAG handles ingestion, transformation, ML training, drift detection, and serving updates — with branching logic for retraining gates.

### 9. Train ML models (standalone)

```bash
python ml/train_models.py
```

### 10. Launch the agentic AI service

```bash
ollama pull llama3.1:8b
python agentic_ai/app.py
```

---

## 📊 Dataset

A synthetic banking transaction dataset (5.3M+ records) is used to demonstrate the platform at scale.

**Download:** [Google Drive](https://drive.google.com/file/d/1Xa-Lte88z_kCO4P5ntrdEVGb3kNzulxs/view?usp=sharing)

```bash
unzip banking-dataset.zip
mv dataset_folder data/
```

---

## 📈 Scale & Highlights

- **Volume:** 5.3M+ synthetic transactions processed end-to-end
- **DAG complexity:** 25-task Airflow pipeline with conditional branching for retraining
- **Model portfolio:** 4 model families across segmentation, anomaly detection, fraud classification, and prediction
- **Agentic AI:** 7-tool semantic router with 4-stage routing logic and anti-hallucination guardrails
- **Lakehouse:** 3-layer medallion architecture (Bronze / Silver / Gold) on Iceberg with idempotent upserts

---

## 🔗 Resources

- **Code Repository:** [GitHub](https://github.com/faisalhaq02/Real-Time-Banking-Transaction-Intelligence-Platform-Using-Streaming-and-Lakehouse-Architecture)
- **Full Project Archive:** [Google Drive](https://drive.google.com/file/d/1g8MpLdHdomAwMdZoPDPenqAinD2yN1-M/view?usp=share_link)
- **Dataset:** [Google Drive](https://drive.google.com/file/d/1Xa-Lte88z_kCO4P5ntrdEVGb3kNzulxs/view?usp=sharing)

---

## 👥 Authors

**Faisal Ul Haque Mohammed**
Master of Applied Computing, Wilfrid Laurier University (April 2026)
[LinkedIn](https://linkedin.com/in/faye02) · [GitHub](https://github.com/faisalhaq02)

**Darshil K Shah**
Master of Applied Computing, Wilfrid Laurier University (April 2026)

---

## ⚠️ Notes

- The `.env` file is intentionally excluded from version control — use your own credentials.
- Ensure Docker and the Kafka broker are running before starting producers/consumers.
- The agentic AI service requires Ollama installed locally; the platform is designed for **local LLM inference** with no external API dependencies.
- This is a graduate capstone built for demonstration purposes; not intended for production financial workloads without further hardening (security review, compliance certification, etc.).

---

## 📜 License

This project is released for academic and portfolio purposes. Please contact the authors for reuse permissions.
