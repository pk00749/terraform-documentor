# EC2 模块输出

output "instance_ids" {
  description = "EC2 实例 ID 列表"
  value       = aws_instance.main[*].id
}

output "instance_arns" {
  description = "EC2 ���例 ARN 列表"
  value       = aws_instance.main[*].arn
}

output "private_ips" {
  description = "EC2 实例私有 IP 地址列表"
  value       = aws_instance.main[*].private_ip
}

output "public_ips" {
  description = "EC2 实例公网 IP 地址列表"
  value       = aws_instance.main[*].public_ip
}

output "elastic_ips" {
  description = "弹性 IP 地址列表"
  value       = aws_eip.main[*].public_ip
}

output "instance_states" {
  description = "EC2 实例状态列表"
  value       = aws_instance.main[*].instance_state
}

output "key_pair_name" {
  description = "使用的 Key Pair 名称"
  value       = var.create_key_pair ? aws_key_pair.main[0].key_name : var.key_name
}

output "security_group_ids" {
  description = "关联的安全组 ID 列表"
  value       = var.security_group_ids
}
