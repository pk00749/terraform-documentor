# EC2 实例模块
# 创建 EC2 实例和相关资源

# 获取最新的 Amazon Linux 2 AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Key Pair（如果需要创建）
resource "aws_key_pair" "main" {
  count = var.create_key_pair ? 1 : 0

  key_name   = "${var.name_prefix}-keypair"
  public_key = var.public_key

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-keypair"
    }
  )
}

# EC2 实例
resource "aws_instance" "main" {
  count = var.instance_count

  ami                    = var.ami_id != "" ? var.ami_id : data.aws_ami.amazon_linux.id
  instance_type          = var.instance_type
  key_name              = var.create_key_pair ? aws_key_pair.main[0].key_name : var.key_name
  vpc_security_group_ids = var.security_group_ids
  subnet_id             = var.subnet_ids[count.index % length(var.subnet_ids)]

  associate_public_ip_address = var.associate_public_ip
  disable_api_termination     = var.disable_api_termination
  monitoring                  = var.enable_detailed_monitoring

  root_block_device {
    volume_type           = var.root_volume_type
    volume_size           = var.root_volume_size
    encrypted             = var.encrypt_root_volume
    delete_on_termination = true

    tags = merge(
      var.tags,
      {
        Name = "${var.name_prefix}-root-volume-${count.index + 1}"
      }
    )
  }

  dynamic "ebs_block_device" {
    for_each = var.additional_ebs_volumes
    content {
      device_name           = ebs_block_device.value.device_name
      volume_type           = ebs_block_device.value.volume_type
      volume_size           = ebs_block_device.value.volume_size
      encrypted             = ebs_block_device.value.encrypted
      delete_on_termination = ebs_block_device.value.delete_on_termination

      tags = merge(
        var.tags,
        {
          Name = "${var.name_prefix}-${ebs_block_device.value.device_name}-${count.index + 1}"
        }
      )
    }
  }

  user_data = var.user_data

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-instance-${count.index + 1}"
    }
  )

  lifecycle {
    ignore_changes = [ami]
  }
}

# Elastic IP（如果需要）
resource "aws_eip" "main" {
  count = var.allocate_eip ? var.instance_count : 0

  instance = aws_instance.main[count.index].id
  domain   = "vpc"

  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-eip-${count.index + 1}"
    }
  )

  depends_on = [aws_instance.main]
}
