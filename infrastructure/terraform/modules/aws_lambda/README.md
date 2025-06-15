<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_iam_policy.ecr_access](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.ecr_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_iam_role_policy_attachment.lambda_basic](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_function_url.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function_url) | resource |
| [aws_iam_policy_document.assume_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_create_function_url"></a> [create\_function\_url](#input\_create\_function\_url) | Flag to determine whether to create a function URL for the Lambda | `bool` | `false` | no |
| <a name="input_description"></a> [description](#input\_description) | A description for the Lambda function | `string` | `"Lambda function for processing stock prices"` | no |
| <a name="input_ecr_repo"></a> [ecr\_repo](#input\_ecr\_repo) | The ECR repository URL | `string` | `""` | no |
| <a name="input_image_tag"></a> [image\_tag](#input\_image\_tag) | The image tag mutability setting for the repository | `string` | `"latest"` | no |
| <a name="input_invoke_mode"></a> [invoke\_mode](#input\_invoke\_mode) | The invoke mode for the Lambda function URL. Valid values are BUFFERED and RESPONSE\_STREAM | `string` | `"BUFFERED"` | no |
| <a name="input_memory_size"></a> [memory\_size](#input\_memory\_size) | The amount of memory available to the Lambda function in MB | `number` | `128` | no |
| <a name="input_name"></a> [name](#input\_name) | The name of the ECR repository | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | A map of tags to add to the ECR repository | `map(string)` | n/a | yes |
| <a name="input_timeout"></a> [timeout](#input\_timeout) | The timeout for the Lambda function in seconds | `number` | `30` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_iam_role_name"></a> [iam\_role\_name](#output\_iam\_role\_name) | The name of the IAM role associated with the Lambda function |
| <a name="output_lambda_arn"></a> [lambda\_arn](#output\_lambda\_arn) | ARN of the Lambda function |
| <a name="output_lambda_function_arn"></a> [lambda\_function\_arn](#output\_lambda\_function\_arn) | The ARN of the Lambda function |
| <a name="output_lambda_function_name"></a> [lambda\_function\_name](#output\_lambda\_function\_name) | The name of the Lambda function |
| <a name="output_lambda_function_url"></a> [lambda\_function\_url](#output\_lambda\_function\_url) | URL of the Lambda function, if enabled |
<!-- END_TF_DOCS -->