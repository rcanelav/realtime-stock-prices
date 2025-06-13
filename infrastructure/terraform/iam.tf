# ################################################################################
#                     IAM Configuration for AWS
# ################################################################################
resource "aws_iam_policy" "allow_bedrock_invoke" {
  name        = "AllowBedrockInvokeModel"
  description = "Allows invoking AWS Bedrock models"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "bedrock:InvokeModel"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_invoke_policy_attachment" {
  role       = module.function.iam_role_name
  policy_arn = aws_iam_policy.allow_bedrock_invoke.arn

  depends_on = [module.function, aws_iam_policy.allow_bedrock_invoke]
}
