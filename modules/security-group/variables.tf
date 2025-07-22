# Security Group 模块变量

variable "vpc_id" {
  description = "VPC ID，安全组将在此 VPC 中创建"
  type        = string
}

variable "name_prefix" {
  description = "资源名称前缀"
  type        = string
  default     = "app"
}

variable "web_ingress_cidrs" {
  description = "允许访问 Web 服务器的 CIDR 块列表"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "ssh_ingress_cidrs" {
  description = "允许 SSH 访问的 CIDR 块列表"
  type        = list(string)
  default     = ["10.0.0.0/8"]
}

variable "enable_ssh" {
  description = "是否启用 SSH 访问"
  type        = bool
  default     = true
}

variable "enable_mysql" {
  description = "是否启用 MySQL/Aurora 数据库端口"
  type        = bool
  default     = false
}

variable "enable_postgresql" {
  description = "是否启用 PostgreSQL 数据库端口"
  type        = bool
  default     = false
}

variable "enable_alb_sg" {
  description = "是否创建 Application Load Balancer 安全组"
  type        = bool
  default     = false
}

variable "tags" {
  description = "要应用到所有资源的标签映射"
  type        = map(string)
  default     = {}
}
