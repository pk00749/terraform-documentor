# S3 模块变量

variable "bucket_name" {
  description = "S3 存储桶名称（必须全局唯一）"
  type        = string
}

variable "force_destroy" {
  description = "是否强制删除非空存储桶"
  type        = bool
  default     = false
}

variable "enable_versioning" {
  description = "是否启用版本控制"
  type        = bool
  default     = true
}

variable "kms_key_id" {
  description = "KMS 密钥 ID 用于加密（留空使用 AES256）"
  type        = string
  default     = ""
}

variable "block_public_acls" {
  description = "是否阻止公共 ACL"
  type        = bool
  default     = true
}

variable "block_public_policy" {
  description = "是否阻止公共策略"
  type        = bool
  default     = true
}

variable "ignore_public_acls" {
  description = "是否忽略公共 ACL"
  type        = bool
  default     = true
}

variable "restrict_public_buckets" {
  description = "是否限制公共存储桶"
  type        = bool
  default     = true
}

variable "bucket_policy" {
  description = "存储桶策略 JSON"
  type        = string
  default     = ""
}

variable "lifecycle_rules" {
  description = "生命周期规则配置列表"
  type = list(object({
    id                                   = string
    enabled                              = bool
    filter_prefix                        = string
    expiration_days                      = number
    noncurrent_version_expiration_days   = number
    transitions = list(object({
      days          = number
      storage_class = string
    }))
  }))
  default = []
}

variable "lambda_notifications" {
  description = "Lambda 函数通知配置列表"
  type = list(object({
    lambda_function_arn = string
    events              = list(string)
    filter_prefix       = string
    filter_suffix       = string
  }))
  default = []
}

variable "topic_notifications" {
  description = "SNS 主题通知配置列表"
  type = list(object({
    topic_arn     = string
    events        = list(string)
    filter_prefix = string
    filter_suffix = string
  }))
  default = []
}

variable "queue_notifications" {
  description = "SQS 队列通知配置列表"
  type = list(object({
    queue_arn     = string
    events        = list(string)
    filter_prefix = string
    filter_suffix = string
  }))
  default = []
}

variable "cors_rules" {
  description = "CORS 规则配置列表"
  type = list(object({
    allowed_headers = list(string)
    allowed_methods = list(string)
    allowed_origins = list(string)
    expose_headers  = list(string)
    max_age_seconds = number
  }))
  default = []
}

variable "tags" {
  description = "要应用到所有资源的标签映射"
  type        = map(string)
  default     = {}
}
