# Real-Time Banking Transaction Intelligence Platform
### Streaming · Lakehouse Architecture · LLM-Powered Analytics

---

## Overview

A production-grade banking intelligence platform that processes **5.3 million transactions representing $15.5 billion in spend** using real-time streaming and lakehouse architecture. The platform combines enterprise data engineering with a multi-layer AI interface powered by local LLMs, semantic routing, and conversation memory.

**Core Capabilities:**
- Real-time transaction ingestion and streaming via Apache Kafka
- Medallion Architecture (Bronze/Silver/Gold) on Azure Data Lake Gen2
- Four ML models: fraud classification, anomaly detection, customer segmentation, spend prediction
- MLOps: model versioning, drift detection, automated retraining gates
- LLM-powered natural language interface with conversation memory
- LangChain semantic intent classification
- Executive BI dashboards via Tableau and a Flask REST API

---

## Architecture

```
Transaction Generator (Kafka Producer)
        ↓
Apache Kafka (Real-Time Streaming)
        ↓
PySpark + Apache Iceberg (Bronze → Silver → Gold)
        ↓
Apache Airflow (25-task DAG orchestration)
        ↓
Azure Data Lake Gen2 + Azure SQL + Blob Storage
        ↓
ML Pipeline (XGBoost · KMeans · Isolation Forest · Random Forest)
        ↓
Agentic AI Layer
├── LangChain Semantic Router (llama3.1:8b)
├── Keyword Fallback Router
├── Ollama LLM Interpretation (llama3.1:8b)
├── Conversation Memory (multi-turn follow-ups)
└── Flask REST API + HTML Frontend
```

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Streaming | Apache Kafka, Structured Streaming |
| Processing | PySpark, Apache Spark, Apache Iceberg |
| Orchestration | Apache Airflow, Docker Compose |
| Cloud | Azure Data Lake Gen2, Azure Blob Storage, Azure SQL, Azure Data Factory |
| ML/MLOps | Scikit-learn, XGBoost, model versioning, drift detection, experiment tracking |
| AI Layer | LangChain, Ollama (llama3.1:8b), Conversation Memory |
| Databases | Azure SQL, DuckDB, Hive Metastore |
| BI | Tableau, Grafana |
| Backend | Python, Flask REST API |
| DevOps | Docker, GitHub Actions, CI/CD, Git |

---

## AI Layer

The platform includes a multi-tier natural language interface — users can ask questions in plain English and receive grounded, data-driven responses.

### How It Works

```
User question
      ↓
Step 1: LangChain semantic routing (llama3.1:8b classifies intent)
      ↓
Step 2: Keyword fallback routing (deterministic fast-path)
      ↓
Step 3: Specialized tool fetches real data from Azure/local files
      ↓
Step 4: Ollama LLM interprets data into natural language
      ↓
Step 5: Response saved to conversation memory
```

### Routing Layers

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Semantic Routing | LangChain + llama3.1:8b | Classifies intent beyond keywords |
| Keyword Routing | Python pattern matching | Fast deterministic fallback |
| LLM Interpretation | Ollama (llama3.1:8b) | Converts raw data to natural language |
| Conversation Memory | Custom memory module | Enables multi-turn follow-up queries |
| Follow-up Detection | Phrase matching | Routes context-dependent queries to memory |

### Example Conversation
```
User:   "show me high risk customers"
System: Returns 13 high-risk customers with scores, amounts, and reasons

User:   "which of those are in Canada?"
System: Filters using conversation memory → C8795 (CA, $21,549) and C4476 (CA, $18,131)
```

### Supported Query Types
- **KPI:** "what is the total spend?", "how is the business doing overall?"
- **Anomaly:** "show suspicious transactions", "anything unusual happening?"
- **Risk:** "show high risk customers", "who should we be worried about?"
- **Segments:** "tell me about our customer groups", "summarize segments"
- **Streaming:** "show latest transactions", "what is the latest timestamp?"
- **Follow-ups:** "which of those are in Canada?", "tell me more about them"

---

## Machine Learning Models

| Model | Algorithm | Purpose |
|-------|-----------|---------|
| Spend Prediction | XGBoost Regressor | Predict future customer spend (R²=0.9986) |
| Customer Segmentation | KMeans + PCA | Group customers by behaviour |
| Anomaly Detection | Isolation Forest | Flag suspicious transactions |
| Risk Scoring | Random Forest | Score customer fraud risk (0–1) |

### MLOps Features
- Model versioning with registry
- Automated drift detection
- Retraining gates and promotion logic
- Experiment tracking

---

## Project Structure

```
├── agentic_ai/
│   ├── app.py                    # Flask REST API entry point
│   ├── agent.py                  # Multi-layer routing engine
│   ├── tools/                    # Specialized analytics tools
│   │   ├── kpi_tool.py           # KPI + Ollama LLM integration
│   │   ├── anomaly_tool.py       # Anomaly detection queries
│   │   ├── risk_tool.py          # Risk scoring queries
│   │   ├── segment_tool.py       # Customer segmentation
│   │   ├── streaming_tool.py     # Live transaction data
│   │   └── label_tool.py         # Customer labels
│   ├── utils/
│   │   ├── ollama_client.py      # Ollama LLM wrapper with memory
│   │   ├── langchain_router.py   # LangChain semantic classifier
│   │   ├── memory.py             # Conversation memory module
│   │   └── data_access.py        # Data loading utilities
│   └── templates/
│       └── index.html            # Chat frontend
├── pipelines/                    # PySpark ETL pipelines
├── ml/                           # ML training scripts
├── airflow_docker/               # Airflow Docker setup
├── producer/                     # Kafka transaction generator
├── consumer/                     # Kafka consumer
├── infra/                        # Azure infrastructure
├── analytics/                    # Analytics scripts
├── bi_exports/                   # BI summary exports
├── Tableu_BI_Dashboards/         # Tableau dashboards
├── requirements.txt
└── README.md
```

---

## Project Links

| Resource | Link |
|----------|------|
| GitHub Repository | https://github.com/faisalhaq02/Real-Time-Banking-Transaction-Intelligence-Platform-Using-Streaming-and-Lakehouse-Architecture |
| Full Project Download | https://drive.google.com/file/d/1g8MpLdHdomAwMdZoPDPenqAinD2yN1-M/view?usp=share_link |
| Dataset Download | https://drive.google.com/file/d/1Xa-Lte88z_kCO4P5ntrdEVGb3kNzulxs/view?usp=sharing |

---

## Setup & Installation

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Apache Kafka
- Ollama (`ollama serve` + `ollama pull llama3.1:8b`)
- Azure account (for cloud storage)

### 1. Clone Repository
```bash
git clone https://github.com/faisalhaq02/Real-Time-Banking-Transaction-Intelligence-Platform-Using-Streaming-and-Lakehouse-Architecture.git
cd Real-Time-Banking-Transaction-Intelligence-Platform-Using-Streaming-and-Lakehouse-Architecture
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the root directory:
```env
AIRFLOW_UID=50000
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=banking_intelligence_db
AZURE_SQL_USERNAME=your_username
AZURE_SQL_PASSWORD=your_password
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

> ⚠️ The `.env` file is excluded from this repository. Never commit credentials to Git.

### 4. Start Ollama (for AI layer)
```bash
ollama serve
ollama pull llama3.1:8b
```

---

## Running the Platform

### Start Infrastructure
```bash
docker compose up -d
```

### Run Kafka Producer
```bash
python producer/transaction_producer_v2.py
```

### Run Kafka Consumer
```bash
python consumer/consumer_file.py
```

### Run Airflow
```bash
cd airflow_docker
docker-compose up
```
Open Airflow UI: http://localhost:8080 and trigger DAGs manually.

### Run ML Training
```bash
python ml/train_models.py
```

### Run AI Chatbot
```bash
python agentic_ai/app.py
```
Open: http://localhost:5001

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Chat frontend |
| `/ask` | POST | Natural language query |
| `/health` | GET | System health check |

### Example API Call
```bash
curl -X POST http://localhost:5001/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "show me high risk customers"}'
```

---

## BI Dashboards

Three Tableau dashboards located in `/Tableu_BI_Dashboards`:

- **Executive Dashboard** — KPIs, total spend, transaction volume, customer metrics
- **Real-Time Dashboard** — Live streaming transaction monitoring
- **Geography Dashboard** — Spend and risk distribution by country and city

---

## Dataset

Download the dataset:
```
https://drive.google.com/file/d/1Xa-Lte88z_kCO4P5ntrdEVGb3kNzulxs/view?usp=sharing
```

```bash
unzip banking-dataset.zip
mv dataset_folder data/
```

---

## Authors

**Faisal Ul Haque Mohammed** · **Darshil K Shah**
Master of Applied Computing · Wilfrid Laurier University

---

## Notes

- `.env` is excluded from the repository — use your own credentials
- Ollama must be running locally for the AI layer to function
- Ensure Docker and Kafka are running before starting the platform
- Azure credentials required for cloud storage integration
- Models and data folders are excluded from Git due to size
