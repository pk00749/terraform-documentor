# Security Group 模块
# 创建常用的安全组配置

# Web 服务器安全组
resource "aws_security_group" "web" {
  name_prefix = "${var.name_prefix}-web-"
  description = "Security group for web servers"
  vpc_id      = var.vpc_id

  # HTTP 入站规则
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = var.web_ingress_cidrs
  }

  # HTTPS 入站规则
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.web_ingress_cidrs
  }

  # SSH 入站规则
  dynamic "ingress" {
    for_each = var.enable_ssh ? [1] : []
    content {
      description = "SSH"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = var.ssh_ingress_cidrs
    }
  }

  # 所有出站流量
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-web-sg"
      Type = "web"
    }
  )
}

# 数据库安全组
resource "aws_security_group" "database" {
  name_prefix = "${var.name_prefix}-db-"
  description = "Security group for database servers"
  vpc_id      = var.vpc_id

  # MySQL/Aurora 入站规则
  dynamic "ingress" {
    for_each = var.enable_mysql ? [1] : []
    content {
      description     = "MySQL/Aurora"
      from_port       = 3306
      to_port         = 3306
      protocol        = "tcp"
      security_groups = [aws_security_group.web.id]
    }
  }

  # PostgreSQL 入站规则
  dynamic "ingress" {
    for_each = var.enable_postgresql ? [1] : []
    content {
      description     = "PostgreSQL"
      from_port       = 5432
      to_port         = 5432
      protocol        = "tcp"
      security_groups = [aws_security_group.web.id]
    }
  }

  # 所有出站流量
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-db-sg"
      Type = "database"
    }
  )
}

# 负载均衡器安全组
resource "aws_security_group" "alb" {
  count = var.enable_alb_sg ? 1 : 0

  name_prefix = "${var.name_prefix}-alb-"
  description = "Security group for Application Load Balancer"
  vpc_id      = var.vpc_id

  # HTTP 入站规则
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS 入站规则
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # 所有出站流量
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-alb-sg"
      Type = "load-balancer"
    }
  )
}
