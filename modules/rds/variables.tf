# RDS 模块变量

variable "name_prefix" {
  description = "资源名称前缀"
  type        = string
  default     = "app"
}

variable "engine" {
  description = "数据库引擎类型"
  type        = string
  default     = "mysql"

  validation {
    condition = contains([
      "mysql", "postgres", "mariadb", "oracle-ee", "oracle-se2", "oracle-se1", "oracle-se", "sqlserver-ee", "sqlserver-se", "sqlserver-ex", "sqlserver-web"
    ], var.engine)
    error_message = "引擎必须是支持的 RDS 引擎类型。"
  }
}

variable "engine_version" {
  description = "数据库引擎版本"
  type        = string
  default     = "8.0"
}

variable "instance_class" {
  description = "RDS 实例类型"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "分配的存储空间（GB）"
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "最大分配存储空间（GB），0 表示禁用自动扩展"
  type        = number
  default     = 100
}

variable "storage_type" {
  description = "存储类型"
  type        = string
  default     = "gp2"
}

variable "storage_encrypted" {
  description = "是否加密存储"
  type        = bool
  default     = true
}

variable "kms_key_id" {
  description = "KMS 密钥 ID 用于存储加密"
  type        = string
  default     = ""
}

variable "database_name" {
  description = "数据库名称"
  type        = string
  default     = "appdb"
}

variable "master_username" {
  description = "主用户名"
  type        = string
  default     = "admin"
}

variable "master_password" {
  description = "主用户密码（留空将自动生成）"
  type        = string
  default     = ""
  sensitive   = true
}

variable "manage_master_user_password" {
  description = "是否让 AWS 管理主用户密码"
  type        = bool
  default     = false
}

variable "database_port" {
  description = "数据库端口"
  type        = number
  default     = 3306
}

variable "subnet_ids" {
  description = "数据库子网 ID 列表"
  type        = list(string)
}

variable "security_group_ids" {
  description = "安全组 ID 列表"
  type        = list(string)
}

variable "publicly_accessible" {
  description = "是否可从公网访问"
  type        = bool
  default     = false
}

variable "create_db_parameter_group" {
  description = "是否创建数据库参数组"
  type        = bool
  default     = false
}

variable "db_parameter_group_name" {
  description = "现有数据库参数组名称"
  type        = string
  default     = ""
}

variable "db_parameter_group_family" {
  description = "数据库参数组族"
  type        = string
  default     = "mysql8.0"
}

variable "db_parameters" {
  description = "数据库参数列表"
  type = list(object({
    name  = string
    value = string
  }))
  default = []
}

variable "backup_retention_period" {
  description = "备份保留天数"
  type        = number
  default     = 7
}

variable "backup_window" {
  description = "备份时间窗口"
  type        = string
  default     = "03:00-04:00"
}

variable "maintenance_window" {
  description = "维护时间窗口"
  type        = string
  default     = "sun:04:00-sun:05:00"
}

variable "monitoring_interval" {
  description = "监控间隔（秒）"
  type        = number
  default     = 0
}

variable "monitoring_role_arn" {
  description = "监控角色 ARN"
  type        = string
  default     = ""
}

variable "enabled_cloudwatch_logs_exports" {
  description = "启用的 CloudWatch 日志导出列表"
  type        = list(string)
  default     = []
}

variable "auto_minor_version_upgrade" {
  description = "是否启用自动小版本升级"
  type        = bool
  default     = true
}

variable "deletion_protection" {
  description = "是否启用删除保护"
  type        = bool
  default     = false
}

variable "skip_final_snapshot" {
  description = "删除时是否跳过最终快照"
  type        = bool
  default     = false
}

variable "tags" {
  description = "要应用到所有资源的标签映射"
  type        = map(string)
  default     = {}
}
