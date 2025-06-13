# ################################################################################
#                   Contains the Lambda Function module
# ################################################################################
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "this" {
  name               = "lambda-operator-${lower(var.name)}"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Add ECR permissions policy
resource "aws_iam_policy" "ecr_access" {
  name        = "lambda-ecr-access-${lower(var.name)}"
  description = "IAM policy for Lambda to pull images from ECR"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecr_policy_attachment" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.ecr_access.arn
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.this.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "this" {
  function_name = lower(var.name)
  description   = var.description
  image_uri     = "${var.ecr_repo}:${var.image_tag}"
  role          = aws_iam_role.this.arn
  timeout       = var.timeout
  package_type  = "Image"

  memory_size = var.memory_size

  lifecycle {
    ignore_changes = [
      image_uri,
    ]
  }
}

resource "aws_lambda_function_url" "this" {
  count              = var.create_function_url ? 1 : 0
  function_name      = aws_lambda_function.this.function_name
  authorization_type = "NONE"
  invoke_mode        = var.invoke_mode
}
