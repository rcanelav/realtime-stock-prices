# ################################################################################
#                     Parameter Store Configuration
# ################################################################################
resource "aws_ssm_parameter" "SERVICE_API_KEY" {
  name        = "/stock-agent/SERVICE_API_KEY"
  description = "API Key for the Stock Agent"
  type        = "SecureString"
  value       = "initial"
  overwrite   = true

  lifecycle {
    ignore_changes = [
      value,
    ]
  }
}

