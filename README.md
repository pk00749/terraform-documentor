# Terraform Modules 项目

这个项目包含多个可重用的 Terraform 模块，用于在 AWS 上构建基础设施。

## 模块列表

- `modules/vpc` - VPC 网络基础设施
- `modules/security-group` - 安全组管理
- `modules/ec2` - EC2 实例部署
- `modules/rds` - RDS 数据库实例
- `modules/s3` - S3 存储桶

## 使用示例

```hcl
# 使用所有模块创建完整的基础设施
module "vpc" {
  source = "./modules/vpc"
  
  vpc_name = "production-vpc"
  vpc_cidr = "10.0.0.0/16"
  # ... 其他配置
}

module "security_group" {
  source = "./modules/security-group"
  
  vpc_id = module.vpc.vpc_id
  # ... 其他配置
}

module "ec2" {
  source = "./modules/ec2"
  
  vpc_id            = module.vpc.vpc_id
  subnet_id         = module.vpc.public_subnet_ids[0]
  security_group_id = module.security_group.web_sg_id
  # ... 其他配置
}
```

## 文档生成

使用以下命令为所有模块生成文档：

```bash
./generate-docs.sh
```

或者为特定模块生成文档：

```bash
./generate-docs.sh modules/vpc
```
