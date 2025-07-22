# EC2 模块变量

variable "name_prefix" {
  description = "资源名称前缀"
  type        = string
  default     = "app"
}

variable "instance_count" {
  description = "要创建的 EC2 实例数量"
  type        = number
  default     = 1

  validation {
    condition     = var.instance_count > 0 && var.instance_count <= 10
    error_message = "实例数量必须在 1 到 10 之间。"
  }
}

variable "instance_type" {
  description = "EC2 实例类型"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "AMI ID（留空将使用最新的 Amazon Linux 2）"
  type        = string
  default     = ""
}

variable "key_name" {
  description = "现有 Key Pair 的名称"
  type        = string
  default     = ""
}

variable "create_key_pair" {
  description = "是否创建新的 Key Pair"
  type        = bool
  default     = false
}

variable "public_key" {
  description = "创建 Key Pair 时使用的公钥内容"
  type        = string
  default     = ""
}

variable "subnet_ids" {
  description = "子网 ID 列表"
  type        = list(string)
}

variable "security_group_ids" {
  description = "安全组 ID 列表"
  type        = list(string)
}

variable "associate_public_ip" {
  description = "是否为实例分配公网 IP"
  type        = bool
  default     = false
}

variable "allocate_eip" {
  description = "是否为实例分配弹性 IP"
  type        = bool
  default     = false
}

variable "disable_api_termination" {
  description = "是否禁用 API 终止保护"
  type        = bool
  default     = false
}

variable "enable_detailed_monitoring" {
  description = "是否启用详细监控"
  type        = bool
  default     = false
}

variable "root_volume_type" {
  description = "根卷类型"
  type        = string
  default     = "gp3"
}

variable "root_volume_size" {
  description = "根卷大小（GB）"
  type        = number
  default     = 20
}

variable "encrypt_root_volume" {
  description = "是否加密根卷"
  type        = bool
  default     = true
}

variable "additional_ebs_volumes" {
  description = "附加 EBS 卷配置列表"
  type = list(object({
    device_name           = string
    volume_type           = string
    volume_size           = number
    encrypted             = bool
    delete_on_termination = bool
  }))
  default = []
}

variable "user_data" {
  description = "实例启动时执行的用户数据脚本"
  type        = string
  default     = ""
}

variable "tags" {
  description = "要应用到所有资源的标签映射"
  type        = map(string)
  default     = {}
}
