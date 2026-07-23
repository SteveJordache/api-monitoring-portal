#!/usr/bin/env bash

set -euo pipefail

usage() {
  echo "Usage: $0 <environment> [host]"
  echo "Allowed environments: dev, test, qa, prod"
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit 1
fi

ENVIRONMENT="$1"
HOST="${2:-127.0.0.1}"

case "$ENVIRONMENT" in
  dev)
    APP_PORT="8001"
    ;;
  test)
    APP_PORT="8002"
    ;;
  qa)
    APP_PORT="8003"
    ;;
  prod)
    APP_PORT="8004"
    ;;
  *)
    echo "Unsupported environment: $ENVIRONMENT"
    usage
    exit 1
    ;;
esac

HEALTH_URL="http://${HOST}:${APP_PORT}/health"
MAX_ATTEMPTS=20
SLEEP_SECONDS=5

echo "Checking ${ENVIRONMENT} environment"
echo "Health URL: ${HEALTH_URL}"

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  echo "Health-check attempt ${attempt}/${MAX_ATTEMPTS}"

  if response="$(curl --fail --silent --show-error "$HEALTH_URL")"; then
    echo "Health check successful."
    echo "$response"
    exit 0
  fi

  sleep "$SLEEP_SECONDS"
done

echo "Health check failed for environment: ${ENVIRONMENT}"
exit 1
