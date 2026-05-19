# End-to-End Data Engineering & Infrastructure Challenge

## Overview

This project simulates a real-time financial market data platform using a fully containerized architecture.

The objective of this project was to design and build an end-to-end data engineering workflow that includes:

- A mock financial market data API
- A resilient ETL pipeline
- Data validation and transformation logic
- MySQL-based persistent storage
- Dockerized infrastructure using Docker Compose

The project is designed to mimic real-world financial data processing systems.

---

# System Architecture

The platform consists of three main components:

## 1. Source Layer — FastAPI Market Data API

A FastAPI-based service generates synthetic market data for financial instruments such as:

- AAPL
- TSLA
- BTC-USD
- ETH-USD
- GOOG

Each API response contains:

- instrument_id
- price
- volume
- timestamp

The API also includes fault injection logic to simulate real-world unreliable systems.

Examples:
- malformed records
- invalid numeric values
- random server failures

---

# 2. ETL Layer — Python Data Pipeline

The ETL pipeline extracts data from the API, validates incoming records, performs transformations, and loads processed data into MySQL.

## Extraction

- API polling using `requests`
- Retry handling using `Tenacity`
- Timeout handling

## Validation

Incoming records are validated using Pydantic schemas.

Invalid records are automatically dropped before processing.

Examples:
- string values in numeric fields
- malformed records
- missing fields

---

# Transformations

## VWAP Calculation

The pipeline calculates VWAP (Volume Weighted Average Price) for each instrument.

Formula:

```text
VWAP = SUM(price × volume) / SUM(volume)
```

---

## Outlier Detection

Records are flagged as outliers when the price deviates more than 15% from the average instrument price within the current batch.

---

# Data Integrity

To maintain reliable data ingestion:

- duplicate records are removed in ETL
- MySQL unique constraints prevent duplicate inserts
- timestamps are normalized before loading

This ensures idempotent and consistent processing.

---

# Logging & Monitoring

Structured logging is implemented to track:

- records processed
- records dropped
- execution time
- extraction failures
- validation failures

---

# 3. Sink Layer — MySQL Database

Processed records are stored in a MySQL database running inside Docker.

The final table stores:

- instrument_id
- price
- volume
- timestamp
- vwap
- is_outlier

---

# Dockerized Infrastructure

The entire platform is containerized using Docker and orchestrated using Docker Compose.

Services include:

- market-api
- market-etl
- market-mysql

All services communicate internally using Docker networking.

---

# Project Structure

```text
market-data-project-2026/
│
├── API/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── etl/
│   ├── etl.py
│   ├── db.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── database/
│   └── init.sql
│
├── .env
├── docker-compose.yml
└── README.md
```

---

# Running the Project

## Prerequisites

- Docker Desktop
- Python 3.11+

---

# Start the Entire Platform

```bash
docker compose up
```

This command automatically starts:

- MySQL database
- FastAPI server
- ETL pipeline

---

# Validate Data Inside MySQL

Connect to the MySQL container:

```bash
docker exec -it market-mysql mysql -u root -p
```

Password:

```text
root
```

Use database:

```sql
USE market_db;
```

Check loaded records:

```sql
SELECT * FROM market_data LIMIT 10;
```

---

# Scaling Considerations

If the platform scaled to billions of records per day, the architecture could evolve using:

- Apache Kafka for streaming ingestion
- Apache Spark for distributed processing
- Amazon S3 / Data Lake storage
- AWS Glue for scalable ETL
- Amazon Redshift or Snowflake for analytics
- Kubernetes for orchestration

This would improve:

- scalability
- distributed processing
- fault tolerance
- streaming performance

---

# Monitoring & Health Checks

In a production environment, monitoring could include:

- API health check endpoints
- Docker health checks
- Prometheus & Grafana dashboards
- CloudWatch monitoring
- ETL execution metrics
- alerting for failures and anomalies

---

# Recovery & Idempotency

To avoid duplicate or partial data loads:

- unique constraints are enforced in MySQL
- ETL performs deduplication before insert
- retries are implemented for temporary failures

Additional production improvements could include:

- checkpointing
- dead-letter queues
- batch tracking
- transactional writes

---

# Technologies Used

- Python
- FastAPI
- Pandas
- Pydantic
- SQLAlchemy
- MySQL
- Docker
- Docker Compose
- Tenacity

---

# Author

Samarth Trigule