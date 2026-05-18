# 📊 MarketSense  
## End-to-End AI Market Intelligence Platform

MarketSense is a production-style financial intelligence platform that ingests real market data, processes financial news through a medallion data architecture, applies machine learning and deep learning for sentiment and movement prediction, and exposes explainable market intelligence through APIs and an interactive dashboard.

---

# Problem Statement

Financial markets generate massive volumes of:

- Breaking news
- Earnings reports
- Macroeconomic events
- Social sentiment
- Price volatility

The challenge:

Traditional platforms show price movement...

but often fail to answer:

> Why is the market moving?  
> What is the current sentiment?  
> What may happen next?

MarketSense solves this by converting unstructured market information into actionable intelligence.

---

# Solution

MarketSense transforms:

```text
Real Market Data
      ↓
Bronze Layer
      ↓
Silver Layer + NLP
      ↓
Gold Layer + Intelligence
      ↓
ML + Deep Learning
      ↓
API + Dashboard + AI Agent
```

---

# System Architecture

```text
Live Market Data (Yahoo Finance + News)
                ↓
         Data Ingestion Layer
                ↓
      Bronze → Silver → Gold
                ↓
    Feature Engineering Layer
                ↓
      ML + FinBERT Models
                ↓
       FastAPI Backend
                ↓
        React Dashboard
                ↓
      AI Reasoning Agent
```

---

# Tech Stack

## Data Engineering
- Python
- Medallion Architecture
- JSON Pipelines
- Docker

## Data Analytics
- Pandas
- Aggregations
- Business KPIs

## Data Science
- Feature Engineering
- Sentiment Analysis

## Machine Learning
- Random Forest Classifier

## Deep Learning
- FinBERT (Transformer NLP)

## Backend
- FastAPI

## Frontend
- React

## Database
- SQLAlchemy
- SQLite (PostgreSQL-ready)

## Cloud Ready
- Docker
- Docker Compose
- Azure-ready architecture

---

# Project Structure

```text
MarketSense/
├── data_sources/
├── processing/
├── intelligence/
├── ml/
├── database/
├── api/
├── agent/
├── frontend/
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Features

## Real Data Ingestion
- Live stock data
- Live financial news

## Bronze Layer
- Raw immutable storage
- Data lineage

## Silver Layer
- Text cleaning
- FinBERT sentiment

## Gold Layer
- Market aggregation
- Sentiment KPIs

## Machine Learning
- Market movement prediction

## AI Agent
Users can ask:

> Why is the market bearish today?

And receive explainable intelligence.

---

# Run Locally

## Clone

```bash
git clone https://github.com/harshr002/MarketSense.git
cd MarketSense
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run Backend

```bash
uvicorn api.main:app --reload
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# API Docs

FastAPI Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Future Enhancements

- PostgreSQL production database
- Kafka real-time streaming
- Azure deployment
- Portfolio intelligence
- Social sentiment ingestion
- RAG + LLM reasoning

---

# Author

**Harsh Roy**  
AI Engineer | Data Engineer | ML Engineer