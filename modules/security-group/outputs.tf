# Security Group 模块输出

output "web_sg_id" {
  description = "Web 服务器安全组的 ID"
  value       = aws_security_group.web.id
}

output "web_sg_arn" {
  description = "Web 服务器安全组的 ARN"
  value       = aws_security_group.web.arn
}

output "database_sg_id" {
  description = "数据库安全组的 ID"
  value       = aws_security_group.database.id
}

output "database_sg_arn" {
  description = "数据库安全组的 ARN"
  value       = aws_security_group.database.arn
}

output "alb_sg_id" {
  description = "ALB 安全组的 ID（如果启用）"
  value       = var.enable_alb_sg ? aws_security_group.alb[0].id : null
}

output "alb_sg_arn" {
  description = "ALB 安全组的 ARN（如果启用）"
  value       = var.enable_alb_sg ? aws_security_group.alb[0].arn : null
}

output "all_security_group_ids" {
  description = "所有创建的安全组 ID 列表"
  value = compact([
    aws_security_group.web.id,
    aws_security_group.database.id,
    var.enable_alb_sg ? aws_security_group.alb[0].id : null
  ])
}
