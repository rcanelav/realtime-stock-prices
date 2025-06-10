# ################################################################################
#                 Contains the ECR module outputs definitions
# ################################################################################
output "repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.ecr_repository.repository_url
}
