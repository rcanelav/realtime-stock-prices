# ################################################################################
#  This file describes the variables that are used in the app
# ################################################################################
variable "AWS_BEDROCK_MODEL_ID" {
  description = "The model ID for the Bedrock model"
  type        = string
}

variable "AWS_REGION" {
  description = "The AWS region to deploy resources in"
  type        = string
}

variable "APP_NAME" {
  description = "The name of the application"
  type        = string
  default     = "stock-prices-agent"
}

variable "CONTAINER_PORT" {
  description = "The port the container listens on"
  type        = number
  default     = 8000
}