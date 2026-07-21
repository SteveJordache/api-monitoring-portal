# API Monitoring Portal — MVP Reached

## Status

The project has reached a functional backend MVP.

The current implementation proves the core product value: a user can define an API monitor, store it persistently, execute it manually, and evaluate whether the monitored endpoint responds with the expected HTTP status.

## Implemented MVP Scope

### Core API functionality

- Create API monitors with `POST /monitors`
- List existing monitors with `GET /monitors`
- Execute a monitor manually with `POST /monitors/{id}/run`
- Compare the actual HTTP status with the expected status
- Measure API response time in milliseconds
- Return a clear `success` or `failure` result
- Return `404 Not Found` for unknown monitor IDs

### Persistence

- PostgreSQL stores monitor configurations
- SQLAlchemy provides database access
- Monitor data remains available after application restart
- PostgreSQL runs locally through Docker Compose
- Database configuration is supplied through `DATABASE_URL`

### Quality and delivery

- Automated tests with `pytest`
- Test isolation through automatic database cleanup
- Containerized backend
- Docker Compose for backend and PostgreSQL
- GitHub Actions CI pipeline
- PostgreSQL service available during CI tests
- Feature branches, pull requests, reviews, and squash merges

## Current Architecture

```text
User / API client
       |
       v
FastAPI backend
       |
       +--> PostgreSQL
       |
       +--> External API endpoint
       |
       v
Monitoring result
```

## Main User Flow

```text
1. Create monitor
2. Persist monitor in PostgreSQL
3. Load monitor configuration
4. Execute HTTP request
5. Measure response time
6. Compare actual and expected status
7. Return monitoring result
```

## MVP Definition

This version is considered a backend MVP because it implements the complete core workflow end to end:

> Define an API endpoint, persist its monitoring configuration, execute the check, and determine whether the endpoint behaves as expected.

The project is not yet a complete end-user product because it does not currently include a frontend, automatic scheduling, alert notifications, or execution history.

## Verified Capabilities

- Backend health endpoint works
- PostgreSQL connection works
- Monitor creation works
- Monitor listing works
- Manual execution works
- Response time measurement works
- Status evaluation works
- Persistence after restart works
- Local tests pass
- GitHub Actions tests pass

## Recommended Repository Structure

```text
mvp/
├── README.md
├── 01-mvp-architecture.png
├── 02-monitor-execution-flow.png
└── 03-mvp-achievements.png
```

## Next Development Stage

The next stage should focus on turning the backend MVP into an operational monitoring product:

1. Store monitoring execution history
2. Add automatic scheduling
3. Handle connection errors and timeouts
4. Add dashboard and status visualization
5. Add alerts and notifications
6. Improve documentation and deployment options
