terraform {
  backend "s3" {
    bucket  = "api-monitoring-portal-tfstate-194772391548"
    key     = "application/terraform.tfstate"
    region  = "eu-central-1"
    encrypt = true
  }
}
