# ################################################################################
#                 Contains the Lambda Function outputs definitions
# ################################################################################
output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = aws_lambda_function.this.function_name
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = aws_lambda_function.this.arn
}

output "lambda_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.this.arn
}

output "lambda_function_url" {
  description = "URL of the Lambda function, if enabled"
  value       = var.create_function_url ? aws_lambda_function_url.this[0].function_url : null
}

