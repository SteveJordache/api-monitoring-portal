# Project Scope

## Project Title

API Monitoring Portal

## Project Summary

The API Monitoring Portal is a web application for configuring, executing, and monitoring REST API test robots.

A user can define an API endpoint, specify the expected HTTP status code, define timeout and response-time thresholds, and execute the robot manually or automatically at a configured interval.

Each execution result is stored in a SQL database and displayed in a dashboard.

## Problem Statement

REST APIs must be checked regularly to detect:

- service unavailability;
- connection errors;
- HTTP errors;
- request timeouts;
- response times above an accepted threshold;
- temporary performance degradation.

Manual checks are inefficient and do not provide a consistent execution history.

The project addresses this problem by automating REST API checks and presenting their results in a central portal.

## Project Objective

The objective is to build a functional MVP that allows a user to:

- configure a REST API monitoring robot;
- execute the robot manually;
- execute the robot automatically at a defined interval;
- validate the returned HTTP status code;
- validate the response time;
- identify timeouts and connection errors;
- store execution results in PostgreSQL;
- display current and historical results in a dashboard.

## Target Users

The application is intended for:

- DevOps engineers;
- cloud engineers;
- system administrators;
- application operators;
- software developers;
- test engineers.

## In Scope

The MVP includes the following functionality:

### Robot Configuration

- Create a REST API robot
- Enter a robot name
- Enter a target URL
- Use the HTTP `GET` method
- Define the expected HTTP status code
- Define a request timeout
- Define the maximum accepted response time
- Enable or disable scheduled execution
- Define an execution interval

### Robot Execution

- Execute a robot manually
- Execute enabled robots automatically
- Measure the response time
- Detect connection errors
- Detect request timeouts
- Compare the actual status code with the expected status code
- Compare the actual response time with the configured threshold

### Result Management

- Store execution results in PostgreSQL
- Store execution date and time
- Store the returned HTTP status code
- Store the measured response time
- Store the execution status
- Store an error message when an execution fails

### Dashboard

- Display configured robots
- Display the latest execution result
- Display `PASS`, `FAIL`, `TIMEOUT`, or `ERROR`
- Display execution history
- Display response times
- Highlight failed executions
- Highlight exceeded response-time thresholds

### Deployment and Delivery

- Run the application locally with Docker Compose
- Deploy the application to AWS EC2
- Use Amazon RDS for PostgreSQL
- Store Docker images in Amazon ECR
- Use GitHub Actions for CI/CD
- Use Amazon CloudWatch for infrastructure logs and basic monitoring

## Out of Scope

The following functionality is not part of the MVP:

- UI browser robots
- Playwright or Selenium test execution
- RabbitMQ robots
- MQTT robots
- Redis
- Kafka or other message brokers
- Kubernetes
- Helm
- Amazon EKS
- user authentication
- role-based access control
- multi-tenancy
- Slack or Microsoft Teams notifications
- advanced alert escalation
- artificial intelligence
- anomaly detection based on historical data
- load testing
- distributed execution workers
- high availability
- automatic horizontal scaling
- mobile application
- support for all HTTP methods
- advanced request scripting
- enterprise secrets management

These features may be considered for future versions.

## Technical Scope

The planned technology stack is:

| Area | Technology |
|---|---|
| Frontend | React |
| Backend | FastAPI |
| Programming language | Python |
| Database | PostgreSQL |
| Scheduling | APScheduler |
| REST client | HTTPX |
| Local deployment | Docker Compose |
| Cloud compute | Amazon EC2 |
| Managed SQL database | Amazon RDS for PostgreSQL |
| Container registry | Amazon ECR |
| CI/CD | GitHub Actions |
| Infrastructure monitoring | Amazon CloudWatch |
| Version control | GitHub |
| Project management | GitHub Projects |

## Main Data Entities

### Robot

A robot contains at least:

- name;
- target URL;
- expected HTTP status code;
- timeout;
- maximum response time;
- execution interval;
- enabled status.

### Execution Result

An execution result contains at least:

- robot identifier;
- execution start time;
- execution end time;
- returned HTTP status code;
- response time;
- execution status;
- error message.

## Execution Statuses

The application uses the following statuses:

- `PASS` — the API responded as expected and within the configured threshold;
- `FAIL` — the API responded, but the response did not meet the expected criteria;
- `TIMEOUT` — the API did not respond within the configured timeout;
- `ERROR` — the request could not be completed because of a technical error.

## Success Criteria

The MVP is considered successful when the following end-to-end scenarios can be demonstrated:

1. A user creates a REST API robot.
2. The robot configuration is stored in PostgreSQL.
3. The user starts the robot manually.
4. The backend sends an HTTP request to the configured endpoint.
5. The response status and response time are evaluated.
6. The execution result is stored in PostgreSQL.
7. The result is displayed in the dashboard.
8. A correct response produces `PASS`.
9. An unexpected HTTP status produces `FAIL`.
10. A slow response above the configured threshold produces `FAIL`.
11. An unavailable endpoint produces `TIMEOUT` or `ERROR`.
12. An enabled robot can be executed automatically according to its configured interval.

## Project Constraints

The project is subject to the following constraints:

- final presentation date: 7 August 2026;
- maximum available working time: approximately three hours per day;
- examination preparation must remain the primary parallel activity;
- the implementation must remain limited to a realistic MVP;
- unnecessary infrastructure complexity must be avoided;
- the project should be stable and demonstrable before the presentation date.

## Deliverables

The planned deliverables are:

- GitHub repository;
- GitHub Project board;
- project documentation;
- source code;
- Docker Compose configuration;
- PostgreSQL database model;
- GitHub Actions workflow;
- AWS deployment;
- execution dashboard;
- demonstration scenarios;
- final presentation.

## Future Enhancements

Possible future extensions include:

- UI robots with Playwright;
- RabbitMQ and MQTT monitoring robots;
- alert notifications by email, Slack, or Microsoft Teams;
- Redis caching;
- distributed workers;
- Kubernetes deployment;
- Helm charts;
- advanced authentication and RBAC;
- anomaly detection;
- Prometheus and Grafana integration;
- multi-environment and multi-tenant support.
