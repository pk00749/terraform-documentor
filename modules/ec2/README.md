<!-- BEGIN_TF_DOCS -->


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
| [aws_eip.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eip) | resource |
| [aws_instance.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance) | resource |
| [aws_key_pair.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/key_pair) | resource |
| [aws_ami.amazon_linux](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/ami) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_additional_ebs_volumes"></a> [additional\_ebs\_volumes](#input\_additional\_ebs\_volumes) | 附加 EBS 卷配置列表 | <pre>list(object({<br/>    device_name           = string<br/>    volume_type           = string<br/>    volume_size           = number<br/>    encrypted             = bool<br/>    delete_on_termination = bool<br/>  }))</pre> | `[]` | no |
| <a name="input_allocate_eip"></a> [allocate\_eip](#input\_allocate\_eip) | 是否为实例分配弹性 IP | `bool` | `false` | no |
| <a name="input_ami_id"></a> [ami\_id](#input\_ami\_id) | AMI ID（留空将使用最新的 Amazon Linux 2） | `string` | `""` | no |
| <a name="input_associate_public_ip"></a> [associate\_public\_ip](#input\_associate\_public\_ip) | 是否为实例分配公网 IP | `bool` | `false` | no |
| <a name="input_create_key_pair"></a> [create\_key\_pair](#input\_create\_key\_pair) | 是否创建新的 Key Pair | `bool` | `false` | no |
| <a name="input_disable_api_termination"></a> [disable\_api\_termination](#input\_disable\_api\_termination) | 是否禁用 API 终止保护 | `bool` | `false` | no |
| <a name="input_enable_detailed_monitoring"></a> [enable\_detailed\_monitoring](#input\_enable\_detailed\_monitoring) | 是否启用详细监控 | `bool` | `false` | no |
| <a name="input_encrypt_root_volume"></a> [encrypt\_root\_volume](#input\_encrypt\_root\_volume) | 是否加密根卷 | `bool` | `true` | no |
| <a name="input_instance_count"></a> [instance\_count](#input\_instance\_count) | 要创建的 EC2 实例数量 | `number` | `1` | no |
| <a name="input_instance_type"></a> [instance\_type](#input\_instance\_type) | EC2 实例类型 | `string` | `"t3.micro"` | no |
| <a name="input_key_name"></a> [key\_name](#input\_key\_name) | 现有 Key Pair 的名称 | `string` | `""` | no |
| <a name="input_name_prefix"></a> [name\_prefix](#input\_name\_prefix) | 资源名称前缀 | `string` | `"app"` | no |
| <a name="input_public_key"></a> [public\_key](#input\_public\_key) | 创建 Key Pair 时使用的公钥内容 | `string` | `""` | no |
| <a name="input_root_volume_size"></a> [root\_volume\_size](#input\_root\_volume\_size) | 根卷大小（GB） | `number` | `20` | no |
| <a name="input_root_volume_type"></a> [root\_volume\_type](#input\_root\_volume\_type) | 根卷类型 | `string` | `"gp3"` | no |
| <a name="input_security_group_ids"></a> [security\_group\_ids](#input\_security\_group\_ids) | 安全组 ID 列表 | `list(string)` | n/a | yes |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | 子网 ID 列表 | `list(string)` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | 要应用到所有资源的标签映射 | `map(string)` | `{}` | no |
| <a name="input_user_data"></a> [user\_data](#input\_user\_data) | 实例启动时执行的用户数据脚本 | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_elastic_ips"></a> [elastic\_ips](#output\_elastic\_ips) | 弹性 IP 地址列表 |
| <a name="output_instance_arns"></a> [instance\_arns](#output\_instance\_arns) | EC2 ���例 ARN 列表 |
| <a name="output_instance_ids"></a> [instance\_ids](#output\_instance\_ids) | EC2 实例 ID 列表 |
| <a name="output_instance_states"></a> [instance\_states](#output\_instance\_states) | EC2 实例状态列表 |
| <a name="output_key_pair_name"></a> [key\_pair\_name](#output\_key\_pair\_name) | 使用的 Key Pair 名称 |
| <a name="output_private_ips"></a> [private\_ips](#output\_private\_ips) | EC2 实例私有 IP 地址列表 |
| <a name="output_public_ips"></a> [public\_ips](#output\_public\_ips) | EC2 实例公网 IP 地址列表 |
| <a name="output_security_group_ids"></a> [security\_group\_ids](#output\_security\_group\_ids) | 关联的安全组 ID 列表 |
<!-- END_TF_DOCS -->