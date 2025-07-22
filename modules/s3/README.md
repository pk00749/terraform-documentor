<!-- BEGIN_TF_DOCS -->


## Important Notes

Please ensure that your Terraform environment is properly configured before using this module.

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0 |
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >=1.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~>5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | ~> 5.0 ~>5.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_s3_bucket.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket_cors_configuration.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_cors_configuration) | resource |
| [aws_s3_bucket_lifecycle_configuration.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_lifecycle_configuration) | resource |
| [aws_s3_bucket_notification.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_notification) | resource |
| [aws_s3_bucket_policy.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_policy) | resource |
| [aws_s3_bucket_public_access_block.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_public_access_block) | resource |
| [aws_s3_bucket_server_side_encryption_configuration.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration) | resource |
| [aws_s3_bucket_versioning.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_versioning) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_block_public_acls"></a> [block\_public\_acls](#input\_block\_public\_acls) | 是否阻止公共 ACL | `bool` | `true` | no |
| <a name="input_block_public_policy"></a> [block\_public\_policy](#input\_block\_public\_policy) | 是否阻止公共策略 | `bool` | `true` | no |
| <a name="input_bucket_name"></a> [bucket\_name](#input\_bucket\_name) | S3 存储桶名称（必须全局唯一） | `string` | n/a | yes |
| <a name="input_bucket_policy"></a> [bucket\_policy](#input\_bucket\_policy) | 存储桶策略 JSON | `string` | `""` | no |
| <a name="input_cors_rules"></a> [cors\_rules](#input\_cors\_rules) | CORS 规则配置列表 | <pre>list(object({<br/>    allowed_headers = list(string)<br/>    allowed_methods = list(string)<br/>    allowed_origins = list(string)<br/>    expose_headers  = list(string)<br/>    max_age_seconds = number<br/>  }))</pre> | `[]` | no |
| <a name="input_enable_versioning"></a> [enable\_versioning](#input\_enable\_versioning) | 是否启用版本控制 | `bool` | `true` | no |
| <a name="input_force_destroy"></a> [force\_destroy](#input\_force\_destroy) | 是否强制删除非空存储桶 | `bool` | `false` | no |
| <a name="input_ignore_public_acls"></a> [ignore\_public\_acls](#input\_ignore\_public\_acls) | 是否忽略公共 ACL | `bool` | `true` | no |
| <a name="input_kms_key_id"></a> [kms\_key\_id](#input\_kms\_key\_id) | KMS 密钥 ID 用于加密（留空使用 AES256） | `string` | `""` | no |
| <a name="input_lambda_notifications"></a> [lambda\_notifications](#input\_lambda\_notifications) | Lambda 函数通知配置列表 | <pre>list(object({<br/>    lambda_function_arn = string<br/>    events              = list(string)<br/>    filter_prefix       = string<br/>    filter_suffix       = string<br/>  }))</pre> | `[]` | no |
| <a name="input_lifecycle_rules"></a> [lifecycle\_rules](#input\_lifecycle\_rules) | 生命周期规则配置列表 | <pre>list(object({<br/>    id                                   = string<br/>    enabled                              = bool<br/>    filter_prefix                        = string<br/>    expiration_days                      = number<br/>    noncurrent_version_expiration_days   = number<br/>    transitions = list(object({<br/>      days          = number<br/>      storage_class = string<br/>    }))<br/>  }))</pre> | `[]` | no |
| <a name="input_queue_notifications"></a> [queue\_notifications](#input\_queue\_notifications) | SQS 队列通知配置列表 | <pre>list(object({<br/>    queue_arn     = string<br/>    events        = list(string)<br/>    filter_prefix = string<br/>    filter_suffix = string<br/>  }))</pre> | `[]` | no |
| <a name="input_restrict_public_buckets"></a> [restrict\_public\_buckets](#input\_restrict\_public\_buckets) | 是否限制公共存储桶 | `bool` | `true` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | 要应用到所有资源的标签映射 | `map(string)` | `{}` | no |
| <a name="input_topic_notifications"></a> [topic\_notifications](#input\_topic\_notifications) | SNS 主题通知配置列表 | <pre>list(object({<br/>    topic_arn     = string<br/>    events        = list(string)<br/>    filter_prefix = string<br/>    filter_suffix = string<br/>  }))</pre> | `[]` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_bucket_arn"></a> [bucket\_arn](#output\_bucket\_arn) | S3 存储桶 ARN |
| <a name="output_bucket_domain_name"></a> [bucket\_domain\_name](#output\_bucket\_domain\_name) | S3 存储桶域名 |
| <a name="output_bucket_hosted_zone_id"></a> [bucket\_hosted\_zone\_id](#output\_bucket\_hosted\_zone\_id) | S3 存储桶托管区域 ID |
| <a name="output_bucket_id"></a> [bucket\_id](#output\_bucket\_id) | S3 存储桶 ID |
| <a name="output_bucket_region"></a> [bucket\_region](#output\_bucket\_region) | S3 存储桶区域 |
| <a name="output_bucket_regional_domain_name"></a> [bucket\_regional\_domain\_name](#output\_bucket\_regional\_domain\_name) | S3 存储桶区域域名 |
| <a name="output_bucket_versioning_status"></a> [bucket\_versioning\_status](#output\_bucket\_versioning\_status) | 存储桶版本控制状态 |
<!-- END_TF_DOCS -->