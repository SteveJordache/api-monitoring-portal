variable "aws_region" {
  description = "AWS region used for the application infrastructure"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name used as prefix for AWS resources"
  type        = string
  default     = "api-monitoring-portal"
}

variable "environment" {
  description = "Shared infrastructure environment name"
  type        = string
  default     = "shared"
}

variable "instance_type" {
  description = "EC2 instance type used for the school project"
  type        = string
  default     = "t3.small"
}

variable "root_volume_size" {
  description = "Root EBS volume size in GiB"
  type        = number
  default     = 20
}

variable "application_ports" {
  description = "Ports exposed for DEV, TEST, QA and PROD"
  type        = list(number)

  default = [
    8001,
    8002,
    8003,
    8004
  ]
}

variable "backup_bucket_name" {
  description = "Persistent S3 bucket used for PostgreSQL backups"
  type        = string
  default     = "api-monitoring-portal-backups-194772391548"
}

variable "common_tags" {
  description = "Common tags applied to application resources"
  type        = map(string)

  default = {
    Project     = "api-monitoring-portal"
    ManagedBy   = "Terraform"
    Environment = "shared"
    Purpose     = "education"
  }
}