# End-to-End Data Engineering & Infrastructure Challenge

## Overview

This project simulates a real-time financial market data platform using a fully containerized architecture.

The objective of this project was to design and build an end-to-end data engineering workflow that includes:

* A mock financial market data API
* A resilient ETL pipeline
* Data validation and transformation logic
* MySQL-based persistent storage
* Dockerized infrastructure using Docker Compose

The project is designed to mimic real-world financial data processing systems.

---

# System Architecture

The platform consists of three main components:

## 1. Source Layer — FastAPI Market Data API

A FastAPI-based service generates synthetic market data for financial instruments such as:

* AAPL
* TSLA
* BTC-USD
* ETH-USD
* GOOG

Each API response contains:

* instrument_id
* price
* volume
* timestamp

The API also includes fault injection logic to simulate real-world unreliable systems.

Examples:

* malformed records
* invalid numeric values
* random server failures

---

# 2. ETL Layer — Python Data Pipeline

The ETL pipeline extracts data from the API, validates incoming records, performs transformations, and loads processed data into MySQL.

## Extraction

* API polling using `requests`
* Retry handling using `Tenacity`
* Timeout handling

## Validation

Incoming records are validated using Pydantic schemas.

Invalid records are automatically dropped before processing.

Examples:

* string values in numeric fields
* malformed records
* missing fields

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

* duplicate records are removed in ETL
* MySQL unique constraints prevent duplicate inserts
* timestamps are normalized before loading

This ensures idempotent and consistent processing.

---

# Logging & Monitoring

Structured logging is implemented to track:

* records processed
* records dropped
* execution time
* extraction failures
* validation failures

---

# 3. Sink Layer — MySQL Database

Processed records are stored in a MySQL database running inside Docker.

The final table stores:

* instrument_id
* price
* volume
* timestamp
* vwap
* is_outlier

---

# Dockerized Infrastructure

The entire platform is containerized using Docker and orchestrated using Docker Compose.

Services include:

* market-api
* market-etl
* market-mysql

All services communicate internally using Docker networking.

---

# Scaling Considerations

If the platform scaled to billions of records per day, the architecture would evolve into a distributed streaming-based data platform.

## Apache Kafka

Kafka could be introduced as the primary ingestion layer.

Instead of directly fetching records from the API, market events would first be published into Kafka topics.

Benefits:

* high-throughput ingestion
* distributed streaming
* replay capability
* fault tolerance
* decoupled architecture

---

## Apache Spark / PySpark

The current Pandas-based ETL could be replaced with Apache Spark for distributed processing.

Spark would provide:

* parallel transformations
* distributed computation
* large-scale batch processing
* real-time streaming support

Spark Structured Streaming could process market events in near real time.

---

## Cloud-Native Storage

For large-scale storage, the architecture could evolve toward:

* Amazon S3
* Delta Lake
* Apache Iceberg

Benefits:

* scalable storage
* partitioned datasets
* schema evolution
* optimized analytics

---

## Analytical Warehousing

Processed datasets could be loaded into:

* Amazon Redshift
* Snowflake
* BigQuery

for reporting and large-scale analytical workloads.

---

## Container Orchestration

For enterprise deployment:

* Kubernetes could manage containers
* Airflow could orchestrate workflows
* CI/CD pipelines could automate deployments

---

# Monitoring & Health Checks

In production systems, health checks and monitoring are critical for reliability and observability.

## API Health Checks

The FastAPI application could expose endpoints such as:

```text
/health
/status
```

These endpoints would verify:

* API availability
* dependency connectivity
* database access

---

## Docker Health Checks

Docker health probes could periodically validate:

* container availability
* memory usage
* service responsiveness

Unhealthy containers could automatically restart.

---

## ETL Monitoring

The ETL pipeline generates structured logs containing:

* records processed
* records dropped
* execution duration
* API failures
* validation failures

---

## Monitoring Stack

Production monitoring could integrate:

* Prometheus
* Grafana
* AWS CloudWatch
* ELK Stack

This would provide:

* centralized logging
* dashboards
* metrics visualization
* real-time observability

---

## Alerting

Automated alerts could trigger for:

* ETL failures
* abnormal drop rates
* API downtime
* delayed processing
* excessive latency

Alerts could be sent through:

* email
* Slack
* PagerDuty

---

# Recovery & Idempotency

If the pipeline fails midway during a large batch, the system must prevent duplicate or partial data loads.

## Current Implementation

The current implementation already supports basic idempotency using:

* ETL-level deduplication
* timestamp normalization
* MySQL unique constraints

This prevents duplicate inserts during retries.

---

## Transaction Management

For larger production systems, database writes could use transactional batch commits.

This ensures:

* complete success
* or full rollback

preventing partial writes.

---

## Checkpointing

Checkpointing could track processing progress using:

* Kafka offsets
* batch IDs
* watermark timestamps

This allows recovery from the last successful checkpoint.

---

## Retry & Replay

Failed batches could safely retry because:

* writes are idempotent
* duplicates are rejected
* processing state is tracked

Kafka replay capability could also reprocess missed events.

---

## Dead Letter Queues (DLQ)

Malformed or failed records could be redirected into a Dead Letter Queue instead of stopping the pipeline.

Benefits:

* isolates bad data
* improves resiliency
* enables later debugging

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

* Docker Desktop
* Python 3.11+

---

# Start the Entire Platform

```bash
docker compose up
```

This command automatically starts:

* MySQL database
* FastAPI server
* ETL pipeline

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

# Technologies Used

* Python
* FastAPI
* Pandas
* Pydantic
* SQLAlchemy
* MySQL
* Docker
* Docker Compose
* Tenacity

---

# Author

Samarth Trigule
