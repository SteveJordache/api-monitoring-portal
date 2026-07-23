#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 <environment> <image-uri> <postgres-password>"
  echo "Allowed environments: dev, test, qa, prod"
}

if [[ $# -ne 3 ]]; then
  usage
  exit 1
fi

ENVIRONMENT="$1"
IMAGE_URI="$2"
GENERATED_POSTGRES_PASSWORD="$3"

case "$ENVIRONMENT" in
  dev)
    APP_PORT="8001"
    POSTGRES_DB="monitoring_dev"
    ;;
  test)
    APP_PORT="8002"
    POSTGRES_DB="monitoring_test"
    ;;
  qa)
    APP_PORT="8003"
    POSTGRES_DB="monitoring_qa"
    ;;
  prod)
    APP_PORT="8004"
    POSTGRES_DB="monitoring_prod"
    ;;
  *)
    echo "Unsupported environment: $ENVIRONMENT"
    usage
    exit 1
    ;;
esac

PROJECT_ROOT="/opt/api-monitoring-portal"
DEPLOYMENT_DIR="${PROJECT_ROOT}/deployment/cloud"
ENV_DIR="${PROJECT_ROOT}/env"
ENV_FILE="${ENV_DIR}/${ENVIRONMENT}.env"
COMPOSE_PROJECT_NAME="api-monitoring-${ENVIRONMENT}"

mkdir -p "$ENV_DIR"

if [[ -f "$ENV_FILE" ]]; then
  EXISTING_POSTGRES_PASSWORD="$(
    grep '^POSTGRES_PASSWORD=' "$ENV_FILE" \
      | head -n 1 \
      | cut -d '=' -f 2-
  )"

  if [[ -z "$EXISTING_POSTGRES_PASSWORD" ]]; then
    echo "Existing environment file does not contain POSTGRES_PASSWORD."
    exit 1
  fi

  POSTGRES_PASSWORD="$EXISTING_POSTGRES_PASSWORD"
  echo "Reusing the existing PostgreSQL password for: ${ENVIRONMENT}"
else
  POSTGRES_PASSWORD="$GENERATED_POSTGRES_PASSWORD"
  echo "Creating the first PostgreSQL configuration for: ${ENVIRONMENT}"
fi

cat > "$ENV_FILE" <<EOF
APP_ENVIRONMENT=${ENVIRONMENT}
APP_PORT=${APP_PORT}
POSTGRES_DB=${POSTGRES_DB}
POSTGRES_USER=monitoring
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
IMAGE_URI=${IMAGE_URI}
EOF

chmod 600 "$ENV_FILE"

aws ecr get-login-password \
  --region "${AWS_REGION:-eu-central-1}" \
  | docker login \
      --username AWS \
      --password-stdin \
      "${IMAGE_URI%%/*}"

docker pull "$IMAGE_URI"

docker compose \
  --project-name "$COMPOSE_PROJECT_NAME" \
  --env-file "$ENV_FILE" \
  --file "${DEPLOYMENT_DIR}/docker-compose.yml" \
  up -d

docker compose \
  --project-name "$COMPOSE_PROJECT_NAME" \
  --env-file "$ENV_FILE" \
  --file "${DEPLOYMENT_DIR}/docker-compose.yml" \
  ps

echo "Deployment completed for environment: ${ENVIRONMENT}"
echo "Application URL: http://localhost:${APP_PORT}"
