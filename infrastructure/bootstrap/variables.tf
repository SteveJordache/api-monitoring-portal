variable "aws_region" {
  description = "AWS region used for the project infrastructure"
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Project name used as prefix for AWS resources"
  type        = string
  default     = "api-monitoring-portal"
}

variable "github_owner" {
  description = "GitHub user or organization that owns the repository"
  type        = string
  default     = "SteveJordache"
}

variable "github_repository" {
  description = "GitHub repository allowed to use the AWS deployment role"
  type        = string
  default     = "api-monitoring-portal"
}

variable "github_branch" {
  description = "GitHub branch allowed to deploy infrastructure"
  type        = string
  default     = "main"
}

variable "common_tags" {
  description = "Common tags applied to AWS resources"
  type        = map(string)

  default = {
    Project     = "api-monitoring-portal"
    ManagedBy   = "Terraform"
    Environment = "bootstrap"
    Purpose     = "education"
  }
}