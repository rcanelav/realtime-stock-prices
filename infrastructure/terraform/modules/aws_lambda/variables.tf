# ################################################################################
#               Contains the Lambda Function variable definitions
# ################################################################################
variable "name" {
  description = "The name of the ECR repository"
  type        = string
}

variable "ecr_repo" {
  description = "The ECR repository URL"
  type        = string
  default     = ""
}

variable "image_tag" {
  description = "The image tag mutability setting for the repository"
  type        = string
  default     = "latest"
}

variable "description" {
  description = "A description for the Lambda function"
  type        = string
  default     = "Lambda function for processing stock prices"
}

variable "tags" {
  description = "A map of tags to add to the ECR repository"
  type        = map(string)
}

variable "timeout" {
  description = "The timeout for the Lambda function in seconds"
  type        = number
  default     = 30
}

variable "create_function_url" {
  description = "Flag to determine whether to create a function URL for the Lambda"
  type        = bool
  default     = false
}

variable "invoke_mode" {
  description = "The invoke mode for the Lambda function URL. Valid values are BUFFERED and RESPONSE_STREAM"
  type        = string
  default     = "BUFFERED"
}

variable "memory_size" {
  description = "The amount of memory available to the Lambda function in MB"
  type        = number
  default     = 128
}
