# RDS 模块输出

output "db_instance_id" {
  description = "RDS 实例标识符"
  value       = aws_db_instance.main.id
}

output "db_instance_arn" {
  description = "RDS 实例 ARN"
  value       = aws_db_instance.main.arn
}

output "db_instance_endpoint" {
  description = "RDS 实例连接端点"
  value       = aws_db_instance.main.endpoint
}

output "db_instance_address" {
  description = "RDS 实例地址"
  value       = aws_db_instance.main.address
}

output "db_instance_port" {
  description = "RDS 实例端口"
  value       = aws_db_instance.main.port
}

output "db_instance_status" {
  description = "RDS 实例状态"
  value       = aws_db_instance.main.status
}

output "db_subnet_group_id" {
  description = "数据库子网组 ID"
  value       = aws_db_subnet_group.main.id
}

output "db_parameter_group_id" {
  description = "数据库参数�� ID"
  value       = var.create_db_parameter_group ? aws_db_parameter_group.main[0].id : null
}

output "master_username" {
  description = "主用户名"
  value       = aws_db_instance.main.username
}

output "generated_password" {
  description = "生成的主用户密码（如果使用随机密码）"
  value       = var.manage_master_user_password ? null : (var.master_password != "" ? null : random_password.master_password[0].result)
  sensitive   = true
}
