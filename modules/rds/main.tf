# RDS 数据库模块
# 创建 RDS 实例和相关资源

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# 随机密码生成
resource "random_password" "master_password" {
  count = var.manage_master_user_password ? 0 : 1

  length  = 16
  special = true
}

# DB 子网组
resource "aws_db_subnet_group" "main" {
  name       = "${var.name_prefix}-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-db-subnet-group"
    }
  )
}

# DB 参数组
resource "aws_db_parameter_group" "main" {
  count = var.create_db_parameter_group ? 1 : 0

  family = var.db_parameter_group_family
  name   = "${var.name_prefix}-db-params"

  dynamic "parameter" {
    for_each = var.db_parameters
    content {
      name  = parameter.value.name
      value = parameter.value.value
    }
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-db-params"
    }
  )
}

# RDS 实例
resource "aws_db_instance" "main" {
  identifier = "${var.name_prefix}-database"

  # 引擎配置
  engine         = var.engine
  engine_version = var.engine_version
  instance_class = var.instance_class

  # 存储配置
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = var.storage_type
  storage_encrypted     = var.storage_encrypted
  kms_key_id           = var.kms_key_id

  # 数据库配置
  db_name  = var.database_name
  username = var.master_username
  password = var.manage_master_user_password ? null : (var.master_password != "" ? var.master_password : random_password.master_password[0].result)

  manage_master_user_password = var.manage_master_user_password
  port                       = var.database_port

  # 网络配置
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = var.security_group_ids
  publicly_accessible   = var.publicly_accessible

  # 参数组
  parameter_group_name = var.create_db_parameter_group ? aws_db_parameter_group.main[0].name : var.db_parameter_group_name

  # 备份配置
  backup_retention_period = var.backup_retention_period
  backup_window          = var.backup_window
  maintenance_window     = var.maintenance_window

  # 监控和日志
  monitoring_interval = var.monitoring_interval
  monitoring_role_arn = var.monitoring_role_arn
  enabled_cloudwatch_logs_exports = var.enabled_cloudwatch_logs_exports

  # 其他配置
  auto_minor_version_upgrade = var.auto_minor_version_upgrade
  deletion_protection       = var.deletion_protection
  skip_final_snapshot      = var.skip_final_snapshot
  final_snapshot_identifier = var.skip_final_snapshot ? null : "${var.name_prefix}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-database"
    }
  )

  lifecycle {
    ignore_changes = [password]
  }
}
