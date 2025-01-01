# ETL Streaming Pipeline Demo

This project demonstrates a modern ETL (Extract, Transform, Load) streaming pipeline using various open-source technologies.

## Architecture Components

- **Apache Airflow**: Workflow orchestration
- **Apache Kafka**: Message broker for real-time data streaming
- **KsqlDB**: Stream processing platform
- **Kafka Connect**: Data integration tool for Kafka
- **MinIO**: S3-compatible object storage
- **Redis**: In-memory data structure store (for Airflow Executor)
- **PostgreSQL**: Relational database (for Airflow metadata)

## Prerequisites

- Docker
- Docker Compose
- Git

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/babanomania/etl-streaming.git
```

2. Set up environment variables (create a `.env` file)

3. Start the services:
```bash
docker compose up -d
```

## Service Endpoints

- Airflow Console: `http://localhost:8080`
- Kafka Console: `http://localhost:8081`
- Kafka Connect UI: `http://localhost:8082`
- MinIO Console: `http://localhost:9001`

## Project Structure

```
.
├── airflow-dags/       # Airflow DAG files
├── generator/          # Data generator service
├── ksql-scripts/      # KsqlDB initialization scripts
├── docker-compose.yml # Service definitions
└── .env              # Environment variables
```

## Data Flow

The data pipeline follows a structured flow through multiple components:

1. The Generator Service acts as the primary data source, producing structured data at regular intervals.
2. Apache Airflow manages and orchestrates the workflow, facilitating data consumption and transmission to Apache Kafka.
3. Apache Kafka serves as the central message broker, handling data ingestion and streaming capabilities.
4. KsqlDB performs real-time stream processing operations on the data flows.
5. Kafka Connect facilitates data export, transferring processed data to MinIO object storage.

This architecture ensures reliable, scalable, and fault-tolerant data processing from source to destination.

## Contributing

Feel free to submit issues and pull requests.

## License

MIT