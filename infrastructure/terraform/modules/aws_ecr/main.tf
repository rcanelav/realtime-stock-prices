# ################################################################################
#         Contains the ECR module for managing AWS ECR repositories.
# ################################################################################
resource "aws_ecr_repository" "ecr_repository" {
  name                 = var.name
  image_tag_mutability = var.image_tag_mutability

  tags = var.tags
}
