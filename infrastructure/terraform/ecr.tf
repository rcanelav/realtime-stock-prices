# ################################################################################
#                         Contains the ECR instances
# ################################################################################
module "ecr" {
  source               = "./modules/aws_ecr"
  name                 = "${var.APP_NAME}-ecr"
  image_tag_mutability = "MUTABLE"

  tags = {
    Name        = "${var.APP_NAME}-ecr"
    Environment = "dev"
    Project     = var.APP_NAME
  }
}
