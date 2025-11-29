# Service Monitoring System

Service status monitoring with FastAPI ingestion endpoint and Elasticsearch storage.

## Architecture

- `app-services`: Container running httpd, RabbitMQ, PostgreSQL
- `injest`: FastAPI service with HTTPS endpoint for status ingestion
- `elasticsearch`: Data storage for service status records
- `monitor.py`: Cron job monitoring services every minute

## Setup

### Generate SSL Certificate and Key

The `injest` service requires SSL certificates for HTTPS. Generate them:

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
```

## Start

```bash
docker compose up -d --build
```

## Test

Check overall health:
```bash
curl -k https://localhost/healthcheck
```

Check specific service:
```bash
curl -k https://localhost/healthcheck/httpd
curl -k https://localhost/healthcheck/rabbitMQ
curl -k https://localhost/healthcheck/postgreSQL
```

Ingest from monitor logs:
```bash
curl -k -X POST https://localhost/add -H "Content-Type: application/json" -d @test1/monitor_logs/httpd-status-20251129-021201.json
```

## Logs

Monitor logs are written to `./monitor_logs/` on the host.
