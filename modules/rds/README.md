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
| <a name="provider_random"></a> [random](#provider\_random) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_db_instance.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance) | resource |
| [aws_db_parameter_group.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_parameter_group) | resource |
| [aws_db_subnet_group.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_subnet_group) | resource |
| [random_password.master_password](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allocated_storage"></a> [allocated\_storage](#input\_allocated\_storage) | 分配的存储空间（GB） | `number` | `20` | no |
| <a name="input_auto_minor_version_upgrade"></a> [auto\_minor\_version\_upgrade](#input\_auto\_minor\_version\_upgrade) | 是否启用自动小版本升级 | `bool` | `true` | no |
| <a name="input_backup_retention_period"></a> [backup\_retention\_period](#input\_backup\_retention\_period) | 备份保留天数 | `number` | `7` | no |
| <a name="input_backup_window"></a> [backup\_window](#input\_backup\_window) | 备份时间窗口 | `string` | `"03:00-04:00"` | no |
| <a name="input_create_db_parameter_group"></a> [create\_db\_parameter\_group](#input\_create\_db\_parameter\_group) | 是否创建数据库参数组 | `bool` | `false` | no |
| <a name="input_database_name"></a> [database\_name](#input\_database\_name) | 数据库名称 | `string` | `"appdb"` | no |
| <a name="input_database_port"></a> [database\_port](#input\_database\_port) | 数据库端口 | `number` | `3306` | no |
| <a name="input_db_parameter_group_family"></a> [db\_parameter\_group\_family](#input\_db\_parameter\_group\_family) | 数据库参数组族 | `string` | `"mysql8.0"` | no |
| <a name="input_db_parameter_group_name"></a> [db\_parameter\_group\_name](#input\_db\_parameter\_group\_name) | 现有数据库参数组名称 | `string` | `""` | no |
| <a name="input_db_parameters"></a> [db\_parameters](#input\_db\_parameters) | 数据库参数列表 | <pre>list(object({<br/>    name  = string<br/>    value = string<br/>  }))</pre> | `[]` | no |
| <a name="input_deletion_protection"></a> [deletion\_protection](#input\_deletion\_protection) | 是否启用删除保护 | `bool` | `false` | no |
| <a name="input_enabled_cloudwatch_logs_exports"></a> [enabled\_cloudwatch\_logs\_exports](#input\_enabled\_cloudwatch\_logs\_exports) | 启用的 CloudWatch 日志导出列表 | `list(string)` | `[]` | no |
| <a name="input_engine"></a> [engine](#input\_engine) | 数据库引擎类型 | `string` | `"mysql"` | no |
| <a name="input_engine_version"></a> [engine\_version](#input\_engine\_version) | 数据库引擎版本 | `string` | `"8.0"` | no |
| <a name="input_instance_class"></a> [instance\_class](#input\_instance\_class) | RDS 实例类型 | `string` | `"db.t3.micro"` | no |
| <a name="input_kms_key_id"></a> [kms\_key\_id](#input\_kms\_key\_id) | KMS 密钥 ID 用于存储加密 | `string` | `""` | no |
| <a name="input_maintenance_window"></a> [maintenance\_window](#input\_maintenance\_window) | 维护时间窗口 | `string` | `"sun:04:00-sun:05:00"` | no |
| <a name="input_manage_master_user_password"></a> [manage\_master\_user\_password](#input\_manage\_master\_user\_password) | 是否让 AWS 管理主用户密码 | `bool` | `false` | no |
| <a name="input_master_password"></a> [master\_password](#input\_master\_password) | 主用户密码（留空将自动生成） | `string` | `""` | no |
| <a name="input_master_username"></a> [master\_username](#input\_master\_username) | 主用户名 | `string` | `"admin"` | no |
| <a name="input_max_allocated_storage"></a> [max\_allocated\_storage](#input\_max\_allocated\_storage) | 最大分配存储空间（GB），0 表示禁用自动扩展 | `number` | `100` | no |
| <a name="input_monitoring_interval"></a> [monitoring\_interval](#input\_monitoring\_interval) | 监控间隔（秒） | `number` | `0` | no |
| <a name="input_monitoring_role_arn"></a> [monitoring\_role\_arn](#input\_monitoring\_role\_arn) | 监控角色 ARN | `string` | `""` | no |
| <a name="input_name_prefix"></a> [name\_prefix](#input\_name\_prefix) | 资源名称前缀 | `string` | `"app"` | no |
| <a name="input_publicly_accessible"></a> [publicly\_accessible](#input\_publicly\_accessible) | 是否可从公网访问 | `bool` | `false` | no |
| <a name="input_security_group_ids"></a> [security\_group\_ids](#input\_security\_group\_ids) | 安全组 ID 列表 | `list(string)` | n/a | yes |
| <a name="input_skip_final_snapshot"></a> [skip\_final\_snapshot](#input\_skip\_final\_snapshot) | 删除时是否跳过最终快照 | `bool` | `false` | no |
| <a name="input_storage_encrypted"></a> [storage\_encrypted](#input\_storage\_encrypted) | 是否加密存储 | `bool` | `true` | no |
| <a name="input_storage_type"></a> [storage\_type](#input\_storage\_type) | 存储类型 | `string` | `"gp2"` | no |
| <a name="input_subnet_ids"></a> [subnet\_ids](#input\_subnet\_ids) | 数据库子网 ID 列表 | `list(string)` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | 要应用到所有资源的标签映射 | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_db_instance_address"></a> [db\_instance\_address](#output\_db\_instance\_address) | RDS 实例地址 |
| <a name="output_db_instance_arn"></a> [db\_instance\_arn](#output\_db\_instance\_arn) | RDS 实例 ARN |
| <a name="output_db_instance_endpoint"></a> [db\_instance\_endpoint](#output\_db\_instance\_endpoint) | RDS 实例连接端点 |
| <a name="output_db_instance_id"></a> [db\_instance\_id](#output\_db\_instance\_id) | RDS 实例标识符 |
| <a name="output_db_instance_port"></a> [db\_instance\_port](#output\_db\_instance\_port) | RDS 实例端口 |
| <a name="output_db_instance_status"></a> [db\_instance\_status](#output\_db\_instance\_status) | RDS 实例状态 |
| <a name="output_db_parameter_group_id"></a> [db\_parameter\_group\_id](#output\_db\_parameter\_group\_id) | 数据库参数�� ID |
| <a name="output_db_subnet_group_id"></a> [db\_subnet\_group\_id](#output\_db\_subnet\_group\_id) | 数据库子网组 ID |
| <a name="output_generated_password"></a> [generated\_password](#output\_generated\_password) | 生成的主用户密码（如果使用随机密码） |
| <a name="output_master_username"></a> [master\_username](#output\_master\_username) | 主用户名 |
<!-- END_TF_DOCS -->