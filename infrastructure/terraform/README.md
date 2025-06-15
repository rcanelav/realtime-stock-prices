<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >=1.2.5 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.99.1 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_ecr"></a> [ecr](#module\_ecr) | ./modules/aws_ecr | n/a |
| <a name="module_function"></a> [function](#module\_function) | ./modules/aws_lambda | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_iam_policy.allow_bedrock_invoke](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role_policy_attachment.bedrock_invoke_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_ssm_parameter.SERVICE_API_KEY](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ssm_parameter) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_APP_NAME"></a> [APP\_NAME](#input\_APP\_NAME) | The name of the application | `string` | `"stock-prices-agent"` | no |
| <a name="input_AWS_BEDROCK_MODEL_ID"></a> [AWS\_BEDROCK\_MODEL\_ID](#input\_AWS\_BEDROCK\_MODEL\_ID) | The model ID for the Bedrock model | `string` | n/a | yes |
| <a name="input_AWS_REGION"></a> [AWS\_REGION](#input\_AWS\_REGION) | The AWS region to deploy resources in | `string` | n/a | yes |
| <a name="input_CONTAINER_PORT"></a> [CONTAINER\_PORT](#input\_CONTAINER\_PORT) | The port the container listens on | `number` | `8000` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->