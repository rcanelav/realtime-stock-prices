# ################################################################################
#                   Contains terraform provider configuration
# ################################################################################
terraform {
  required_version = ">=1.2.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "tf-state-backend-tech42"
    key            = "terraform.tfstate"
    region         = "eu-west-2"
    encrypt        = true
    dynamodb_table = "tf-state-lock"
  }
}
