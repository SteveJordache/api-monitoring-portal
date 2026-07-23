output "aws_account_id" {
  description = "AWS account ID used by the application infrastructure"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "AWS region used by the application infrastructure"
  value       = var.aws_region
}

output "vpc_id" {
  description = "ID of the application VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "ID of the public subnet"
  value       = aws_subnet.public.id
}

output "security_group_id" {
  description = "ID of the application security group"
  value       = aws_security_group.application.id
}

output "ec2_instance_id" {
  description = "ID of the application EC2 instance"
  value       = aws_instance.application.id
}

output "ec2_public_ip" {
  description = "Public IP address of the application EC2 instance"
  value       = aws_instance.application.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS name of the application EC2 instance"
  value       = aws_instance.application.public_dns
}

output "ecr_repository_name" {
  description = "Name of the ECR repository"
  value       = aws_ecr_repository.application.name
}

output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.application.repository_url
}

output "backup_bucket_name" {
  description = "Persistent S3 bucket used for PostgreSQL backups"
  value       = var.backup_bucket_name
}

output "application_urls" {
  description = "Public URLs for the logical application environments"

  value = {
    dev  = "http://${aws_instance.application.public_ip}:8001"
    test = "http://${aws_instance.application.public_ip}:8002"
    qa   = "http://${aws_instance.application.public_ip}:8003"
    prod = "http://${aws_instance.application.public_ip}:8004"
  }
}
