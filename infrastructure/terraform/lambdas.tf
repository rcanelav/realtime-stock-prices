# ################################################################################
#                     Contains the Lambda function instances
# ################################################################################
module "function" {
  source              = "./modules/aws_lambda"
  name                = var.APP_NAME
  ecr_repo            = module.ecr.repository_url
  timeout             = 120
  create_function_url = true
  invoke_mode         = "RESPONSE_STREAM"

  tags = {
    Name        = "${var.APP_NAME}"
    Environment = "dev"
    Project     = var.APP_NAME
  }
}
