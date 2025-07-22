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
| [aws_security_group.alb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_security_group.database](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_security_group.web](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_enable_alb_sg"></a> [enable\_alb\_sg](#input\_enable\_alb\_sg) | 是否创建 Application Load Balancer 安全组 | `bool` | `false` | no |
| <a name="input_enable_mysql"></a> [enable\_mysql](#input\_enable\_mysql) | 是否启用 MySQL/Aurora 数据库端口 | `bool` | `false` | no |
| <a name="input_enable_postgresql"></a> [enable\_postgresql](#input\_enable\_postgresql) | 是否启用 PostgreSQL 数据库端口 | `bool` | `false` | no |
| <a name="input_enable_ssh"></a> [enable\_ssh](#input\_enable\_ssh) | 是否启用 SSH 访问 | `bool` | `true` | no |
| <a name="input_name_prefix"></a> [name\_prefix](#input\_name\_prefix) | 资源名称前缀 | `string` | `"app"` | no |
| <a name="input_ssh_ingress_cidrs"></a> [ssh\_ingress\_cidrs](#input\_ssh\_ingress\_cidrs) | 允许 SSH 访问的 CIDR 块列表 | `list(string)` | <pre>[<br/>  "10.0.0.0/8"<br/>]</pre> | no |
| <a name="input_tags"></a> [tags](#input\_tags) | 要应用到所有资源的标签映射 | `map(string)` | `{}` | no |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | VPC ID，安全组将在此 VPC 中创建 | `string` | n/a | yes |
| <a name="input_web_ingress_cidrs"></a> [web\_ingress\_cidrs](#input\_web\_ingress\_cidrs) | 允许访问 Web 服务器的 CIDR 块列表 | `list(string)` | <pre>[<br/>  "0.0.0.0/0"<br/>]</pre> | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_alb_sg_arn"></a> [alb\_sg\_arn](#output\_alb\_sg\_arn) | ALB 安全组的 ARN（如果启用） |
| <a name="output_alb_sg_id"></a> [alb\_sg\_id](#output\_alb\_sg\_id) | ALB 安全组的 ID（如果启用） |
| <a name="output_all_security_group_ids"></a> [all\_security\_group\_ids](#output\_all\_security\_group\_ids) | 所有创建的安全组 ID 列表 |
| <a name="output_database_sg_arn"></a> [database\_sg\_arn](#output\_database\_sg\_arn) | 数据库安全组的 ARN |
| <a name="output_database_sg_id"></a> [database\_sg\_id](#output\_database\_sg\_id) | 数据库安全组的 ID |
| <a name="output_web_sg_arn"></a> [web\_sg\_arn](#output\_web\_sg\_arn) | Web 服务器安全组的 ARN |
| <a name="output_web_sg_id"></a> [web\_sg\_id](#output\_web\_sg\_id) | Web 服务器安全组的 ID |
<!-- END_TF_DOCS -->