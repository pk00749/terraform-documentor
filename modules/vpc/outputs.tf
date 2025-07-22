# VPC 输出变量

output "vpc_id" {
  description = "VPC 的 ID"
  value       = aws_vpc.main.id
}

output "vpc_arn" {
  description = "VPC 的 ARN"
  value       = aws_vpc.main.arn
}

output "vpc_cidr_block" {
  description = "VPC 的 CIDR 块"
  value       = aws_vpc.main.cidr_block
}

output "internet_gateway_id" {
  description = "Internet Gateway 的 ID"
  value       = aws_internet_gateway.main.id
}

output "public_subnet_ids" {
  description = "公共子网 ID 列表"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "私有子网 ID 列表"
  value       = aws_subnet.private[*].id
}

output "public_subnet_cidrs" {
  description = "公共子网 CIDR 块列表"
  value       = aws_subnet.public[*].cidr_block
}

output "private_subnet_cidrs" {
  description = "私有子网 CIDR 块列表"
  value       = aws_subnet.private[*].cidr_block
}

output "public_route_table_id" {
  description = "公共路由表的 ID"
  value       = aws_route_table.public.id
}

output "private_route_table_ids" {
  description = "私有路由表 ID 列表"
  value       = aws_route_table.private[*].id
}

output "nat_gateway_ids" {
  description = "NAT Gateway ID 列表"
  value       = aws_nat_gateway.main[*].id
}

output "nat_eip_public_ips" {
  description = "NAT Gateway 弹性 IP 的公共 IP 地址列表"
  value       = aws_eip.nat[*].public_ip
}

output "availability_zones" {
  description = "使用的可用区列表"
  value       = var.availability_zones
}
