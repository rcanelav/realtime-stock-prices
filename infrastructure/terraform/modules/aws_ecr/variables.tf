# ################################################################################
#               Contains the ECR module variables definitions
# ################################################################################
variable "name" {
  description = "The name of the ECR repository"
  type        = string
}

variable "image_tag_mutability" {
  description = "The image tag mutability setting for the repository"
  type        = string
  default     = "MUTABLE"
}


variable "tags" {
  description = "A map of tags to add to the ECR repository"
  type        = map(string)
}
