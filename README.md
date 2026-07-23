# API Monitoring Portal

A browser-based application for creating, scheduling and executing REST API monitors.

The project demonstrates a complete local DevOps workflow with FastAPI, PostgreSQL, Docker Compose, automated tests, GitHub Actions, Prometheus, Grafana and Alertmanager.

---

## Project goals

The application allows users to:

- create REST API monitors;
- validate expected HTTP status codes;
- run monitors manually;
- execute active monitors automatically;
- store execution results in PostgreSQL;
- display monitor status and execution history;
- expose Prometheus metrics;
- visualize metrics in Grafana;
- trigger alerts for failed monitor executions.

---

## Current MVP status

The local MVP is complete.

Implemented features:

- health-check endpoint;
- monitor creation and listing;
- input validation with Pydantic;
- manual monitor execution;
- PostgreSQL persistence;
- execution history;
- timeout and network-error handling;
- scheduled execution with APScheduler;
- active and inactive monitor states;
- browser-based web frontend;
- dashboard summary;
- automatic frontend refresh;
- Prometheus metrics;
- Grafana dashboard provisioning;
- Alertmanager integration;
- automated backend tests;
- Docker Compose environment;
- GitHub Actions CI pipeline.

AWS deployment, Terraform and multi-environment deployment are planned for the next project phase.

---

## Technology stack

### Application

- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Psycopg
- HTTPX
- APScheduler
- Jinja2

### Frontend

- HTML
- CSS
- Vanilla JavaScript
- Jinja2 templates

### Testing and CI

- Pytest
- FastAPI TestClient
- GitHub Actions

### Containers and observability

- Docker
- Docker Compose
- Prometheus
- Grafana
- Alertmanager

---

## Architecture

```text
Browser
   |
   v
FastAPI Web Application
   |
   +--> REST API endpoints
   |
   +--> Jinja2 frontend
   |
   +--> APScheduler
   |
   +--> PostgreSQL
   |
   +--> Prometheus metrics
              |
              v
         Prometheus
          /      \
         v        v
     Grafana   Alertmanager
```

---

## Project structure

```text
api-monitoring-portal/
├── .github/
│   └── workflows/
├── backend/
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── metrics.py
│   │   ├── models.py
│   │   ├── scheduler.py
│   │   ├── services.py
│   │   ├── static/
│   │   │   ├── app.js
│   │   │   └── styles.css
│   │   └── templates/
│   │       └── index.html
│   ├── tests/
│   ├── Dockerfile
│   ├── pytest.ini
│   ├── requirements.txt
│   └── requirements-dev.txt
├── deployment/
│   ├── alertmanager/
│   │   └── alertmanager.yml
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── provisioning/
│   ├── prometheus/
│   │   ├── alert_rules.yml
│   │   └── prometheus.yml
│   └── docker-compose.yml
└── README.md
```

---

## Application endpoints

### Web interface

```text
GET /
```

Opens the browser-based monitoring portal.

### Health check

```text
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "api-monitoring-backend"
}
```

### Create monitor

```text
POST /monitors
```

Example request:

```json
{
  "name": "Example API",
  "url": "https://example.com/",
  "method": "GET",
  "expected_status": 200,
  "interval_seconds": 60,
  "is_active": true
}
```

### List monitors

```text
GET /monitors
```

### Run monitor manually

```text
POST /monitors/{monitor_id}/run
```

### View execution history

```text
GET /monitors/{monitor_id}/results
```

### Dashboard summary

```text
GET /dashboard/summary
```

Example response:

```json
{
  "total": 4,
  "up": 2,
  "down": 1,
  "inactive": 1,
  "not_checked": 0
}
```

### Prometheus metrics

```text
GET /metrics
```

---

## Run the complete environment with Docker Compose

From the repository root:

```bash
docker compose -f deployment/docker-compose.yml up -d --build
```

Check all services:

```bash
docker compose -f deployment/docker-compose.yml ps
```

Expected services:

```text
api-monitoring-postgres
api-monitoring-backend
api-monitoring-prometheus
api-monitoring-grafana
api-monitoring-alertmanager
```

Stop the environment:

```bash
docker compose -f deployment/docker-compose.yml down
```

Do not use `-v` if you want to preserve the PostgreSQL, Prometheus and Grafana volumes.

---

## Service URLs

| Service | URL |
|---|---|
| API Monitoring Portal | http://127.0.0.1:8000 |
| FastAPI documentation | http://127.0.0.1:8000/docs |
| Prometheus | http://127.0.0.1:9090 |
| Grafana | http://127.0.0.1:3000 |
| Alertmanager | http://127.0.0.1:9093 |

Default Grafana credentials:

```text
Username: admin
Password: admin
```

These credentials are intended only for local development.

---

## Run the backend locally

Start PostgreSQL from Docker:

```bash
docker compose -f deployment/docker-compose.yml up -d postgres
```

Enter the backend directory:

```bash
cd backend
```

Create the virtual environment if it does not exist:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## Run tests

PostgreSQL must be running.

From the `backend` directory:

```bash
source .venv/bin/activate
python -m pytest -v
```

The test suite covers:

- health endpoint;
- monitor creation and listing;
- manual execution;
- unknown monitor handling;
- execution result persistence;
- timeout handling;
- network-error handling;
- scheduler behavior;
- dashboard summary.

---

## Prometheus metrics

The application exposes custom metrics including:

```text
api_monitoring_http_requests_total
api_monitoring_http_request_duration_seconds
api_monitoring_monitor_executions_total
api_monitoring_monitor_execution_duration_seconds
api_monitoring_monitor_execution_failures_total
```

Example Prometheus query:

```promql
sum(rate(api_monitoring_http_requests_total[5m]))
```

Monitor execution totals:

```promql
sum by (success) (
  api_monitoring_monitor_executions_total
)
```

---

## Grafana dashboard

Grafana is provisioned automatically from files stored in:

```text
deployment/grafana/
```

The dashboard includes panels for:

- total HTTP requests;
- HTTP requests per second;
- monitor executions by result;
- monitor execution failures;
- average monitor response time.

Dashboard path:

```text
Dashboards → API Monitoring → API Monitoring Portal
```

---

## Alertmanager

Prometheus evaluates the rule:

```text
ApiMonitorExecutionFailure
```

An alert is triggered when the following metric increases:

```promql
increase(api_monitoring_monitor_execution_failures_total[2m]) > 0
```

The alert includes:

- monitor ID;
- error type;
- severity;
- summary;
- description.

Supported failure types include:

```text
unexpected_status
timeout
request_error
```

---

## Controlled alert test

1. Open the portal at `http://127.0.0.1:8000`.
2. Create a monitor with URL `https://example.com/` and expected status `500`.
3. Click `Run now`.
4. Open Prometheus alerts at `http://127.0.0.1:9090/alerts`.
5. Wait for the state to change from `Pending` to `Firing`.
6. Open Alertmanager at `http://127.0.0.1:9093`.

The alert should appear with the monitor ID and failure type.

---

## Local demo scenario

1. Start the full Docker Compose stack.
2. Open the API Monitoring Portal.
3. Create an active monitor with expected status `200`.
4. Run the monitor manually.
5. Show the `UP` status and execution history.
6. Show automatic scheduler executions.
7. Open the dashboard summary.
8. Open Prometheus metrics.
9. Open the provisioned Grafana dashboard.
10. Create a controlled failure with expected status `500`.
11. Show the alert in Prometheus.
12. Show the alert in Alertmanager.
13. Run the automated test suite.
14. Show the GitHub Actions pipeline and pull request history.

---

## Development workflow

```text
Issue
  ↓
Feature branch
  ↓
Implementation
  ↓
Automated tests
  ↓
Pull request
  ↓
GitHub Actions
  ↓
Squash and merge
```

The complete development history can be reviewed through commits, issues, pull requests, pull request descriptions and GitHub Actions runs.

---

## Planned next phase

The next phase will add AWS deployment and infrastructure automation.

Planned components:

- Terraform;
- AWS EC2;
- Amazon ECR;
- GitHub Actions deployment;
- GitHub OIDC authentication;
- DEV, TEST, QA and PROD logical environments;
- automated promotion between environments;
- backup and restore using Amazon S3;
- controlled infrastructure destroy workflow;
- CloudWatch logging and monitoring.

The cloud design will prioritize low cost and use a shared EC2-based architecture for the school project.

---

## Repository

https://github.com/SteveJordache/api-monitoring-portal

---

## License

This project is currently intended for educational and demonstration purposes.
