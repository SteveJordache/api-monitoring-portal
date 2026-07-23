#!/usr/bin/env bash

set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update

apt-get install -y \
  ca-certificates \
  curl \
  docker.io \
  docker-compose-v2 \
  git \
  jq \
  postgresql-client \
  unzip

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" \
  -o "/tmp/awscliv2.zip"

cd /tmp
unzip -q awscliv2.zip
./aws/install

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

mkdir -p /opt/api-monitoring-portal
chown ubuntu:ubuntu /opt/api-monitoring-portal

cat > /etc/api-monitoring-portal-environment <<EOF
PROJECT_NAME=${project_name}
AWS_REGION=${aws_region}
BACKUP_BUCKET=${backup_bucket_name}
ECR_REPOSITORY_URL=${ecr_repository_url}
EOF

chmod 600 /etc/api-monitoring-portal-environment

docker --version
docker compose version
aws --version

touch /var/log/api-monitoring-user-data-complete