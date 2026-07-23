output "aws_account_id" {
  description = "AWS account ID used by the project"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "AWS region used by the project"
  value       = var.aws_region
}

output "terraform_state_bucket_name" {
  description = "Name of the S3 bucket used for Terraform remote state"
  value       = aws_s3_bucket.terraform_state.bucket
}

output "database_backup_bucket_name" {
  description = "Name of the S3 bucket used for PostgreSQL backups"
  value       = aws_s3_bucket.database_backups.bucket
}

output "github_actions_role_name" {
  description = "Name of the IAM role used by GitHub Actions"
  value       = aws_iam_role.github_actions.name
}

output "github_actions_role_arn" {
  description = "ARN of the IAM role used by GitHub Actions"
  value       = aws_iam_role.github_actions.arn
}

output "github_oidc_provider_arn" {
  description = "ARN of the GitHub OpenID Connect provider"
  value       = aws_iam_openid_connect_provider.github.arn
}