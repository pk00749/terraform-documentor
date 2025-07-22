# VPC 配置变量

variable "vpc_name" {
  description = "VPC 的名称"
  type        = string
  default     = "main-vpc"
}

variable "vpc_cidr" {
  description = "VPC 的 CIDR 块"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR 必须是有效的 IPv4 CIDR 块。"
  }
}

variable "availability_zones" {
  description = "要使用的可用区列表"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

variable "public_subnet_cidrs" {
  description = "公共子网的 CIDR 块列表"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

  validation {
    condition = alltrue([
      for cidr in var.public_subnet_cidrs : can(cidrhost(cidr, 0))
    ])
    error_message = "所有公共子网 CIDR 必须是有效的 IPv4 CIDR 块。"
  }
}

variable "private_subnet_cidrs" {
  description = "私有子网的 CIDR 块列表"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  validation {
    condition = alltrue([
      for cidr in var.private_subnet_cidrs : can(cidrhost(cidr, 0))
    ])
    error_message = "所有私有子网 CIDR 必须是有效的 IPv4 CIDR 块。"
  }
}

variable "enable_dns_hostnames" {
  description = "是否在 VPC 中启用 DNS 主机名"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "是否在 VPC 中启用 DNS 支持"
  type        = bool
  default     = true
}

variable "enable_nat_gateway" {
  description = "是否为私有子网创建 NAT Gateway"
  type        = bool
  default     = true
}

variable "tags" {
  description = "要应用到所有资源的标签映射"
  type        = map(string)
  default     = {}
}
