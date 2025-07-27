# 产品需求文档 (PRD) - Terraform模块自动生成工具

## 1. 项目概述

### 1.1 项目背景
当前项目包含了alibabacloudstack provider的完整文档，位于`website/docs/r/`目录下，包含200+个资源类型的详细文档。为了提高开发效率，需要开发一个自动化工具，根据这些文档自动生成标准化的terraform模块。

### 1.2 项目目标
- 自动解析website下的terraform资源文档
- 生成标准化的terraform模块结构
- 提供灵活的参数配置和模板定制
- 支持批量生成和单个资源生成

## 2. 功能需求

### 2.1 核心功能

#### 2.1.1 文档解析功能
- **输入**: website/docs/r/目录下的.html.markdown文件
- **解析内容**:
  - 资源名称和类型
  - Argument Reference部分的参数定义
  - 参数的必需性(Required/Optional)
  - 参数的默认值（从文档描述中提取）
  - 参数的描述信息
  - 参数的类型(string, number, bool, list, map等)
  - Example Usage部分的示例代码

#### 2.1.2 模块生成功能
为每个资源生成完整的terraform模块，包含以下双层结构：

**modules/alibabacloudstack/{service}/{resource}/目录包含：**
- `main.tf` - 主要资源定义
- `variables.tf` - 输入变量定义
- `outputs.tf` - 输出变量定义
- `versions.tf` - provider版本约束
- `README.md` - 模块使用文档

**example_alibabacloudstack/{service}/{resource}/目录包含：**
- `main.tf` - 调用模块的示例代码
- `variables.tf` - 与模块相同的变量定义
- `outputs.tf` - 从模块输出的变量定义
- `versions.tf` - provider版本约束
- `README.md` - 与modules目录下完全相同的使用文档
- `env_vars/{resource}.tfvars` - 参数配置文件

#### 2.1.3 目录结构管理
- 按服务类型自动分类(如ecs, vpc, rds等)
- 生成路径: 
  - 实际模块：`modules/alibabacloudstack/{service}/{resource}/`
  - 调用示例：`example_alibabacloudstack/{service}/{resource}/`
- 支持嵌套目录结构

### 2.2 技术要求

#### 2.2.1 脚本功能
- 支持Python开发
- 支持命令行参数
- 支持配置文件
- 提供详细的日志输出

#### 2.2.2 解析规则
- 使用正则表达式解析markdown格式
- 智能识别参数类型
- 处理嵌套对象和列表类型
- 支持ForceNew、Sensitive等特殊标记
- 从参数描述中提取默认值信息

#### 2.2.3 模板生成规则
- **Resource命名格式**: `resource "alibabacloudstack_ecs_instance" "ecs_instance"`
- variables.tf中Required参数不设置default值
- variables.tf中Optional参数根据文档描述设置适当的default值
- 所有参数description使用英文原文
- main.tf包含完整的资源配置
- outputs.tf导出关键属性
- 支持tags的标准化处理
- **README.md文件**: modules和example_alibabacloudstack目录下的README.md内容完全相同

### 2.3 脚本参数设计

#### 2.3.1 批量生成模式
```bash
python generate-alibabacloudstack-modules.py --mode batch --input-dir website/docs/r/ --output-dir modules/alibabacloudstack/ --example-dir example_alibabacloudstack/
```

#### 2.3.2 单个资源生成模式
```bash
python generate-alibabacloudstack-modules.py --mode single --resource ecs_instance --input-file website/docs/r/ecs_instance.html.markdown --output-dir modules/alibabacloudstack/ecs/ --example-dir example_alibabacloudstack/ecs/
```

#### 2.3.3 可选参数
- `--force` - 强制覆盖已存在的模块
- `--template-dir` - 自定义模板目录
- `--config` - 指定配置文件
- `--verbose` - 详细输出模式
- `--dry-run` - 预览模式，不实际生成文件

## 3. 输出规范

### 3.1 文件结构示例
```
modules/alibabacloudstack/
├── ecs/
│   ├── instance/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── versions.tf
│   │   └── README.md
│   └── disk/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── versions.tf
│       └── README.md
└── vpc/
    └── vpc/
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
        ├── versions.tf
        └── README.md

example_alibabacloudstack/
├── ecs/
│   ├── instance/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── versions.tf
│   │   ├── README.md
│   │   └── env_vars/
│   │       └── ecs_instance.tfvars
│   └── disk/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── versions.tf
│       ├── README.md
│       └── env_vars/
│           └── ecs_disk.tfvars
└── vpc/
    └── vpc/
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
        ├── versions.tf
        ├── README.md
        └── env_vars/
            └── vpc_vpc.tfvars
```

### 3.2 文件内容规范

#### 3.2.1 variables.tf
```hcl
variable "instance_name" {
  type        = string
  description = "The name of the ECS instance. This can be a string of 2 to 128 characters and cannot begin with http:// or https://."
  default     = null  # 仅对Optional参数设置default
}

variable "image_id" {
  type        = string
  description = "The image ID used for the instance."
  # Required参数不设置default
}
```

#### 3.2.2 main.tf (modules目录)
```hcl
resource "alibabacloudstack_ecs_instance" "ecs_instance" {
  # 包含所有可配置的参数
  instance_name    = var.instance_name
  image_id         = var.image_id
  instance_type    = var.instance_type
  # ... 其他参数
  
  # 支持动态块
  dynamic "data_disks" {
    for_each = var.data_disks
    content {
      category = data_disks.value.category
      size     = data_disks.value.size
      # ... 其他嵌套参数
    }
  }
}
```

#### 3.2.3 main.tf (example_alibabacloudstack目录)
```hcl
# Example usage of ecs_instance module

module "instance" {
  source = "../../../modules/alibabacloudstack/ecs/instance"
  
  # 引用所有变量
  instance_name = var.instance_name
  image_id      = var.image_id
  instance_type = var.instance_type
  # ... 其他参数
}
```

#### 3.2.4 outputs.tf
```hcl
output "instance_id" {
  description = "The ID of the ECS instance"
  value       = alibabacloudstack_ecs_instance.ecs_instance.id  # modules目录
  # 或者
  value       = module.instance.id  # example_alibabacloudstack目录
}
```

#### 3.2.5 README.md (两个目录内容相同)
```markdown
# alibabacloudstack_ecs_instance Module

Provides a ecs Instance resource.

## Usage

\```hcl
module "ecs_instance" {
  source = "./modules/alibabacloudstack/ecs/instance"
  
  # Required variables
  image_id      = "example_value"
  instance_type = "example_value"
}
\```

## Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| instance_name | The name of the ECS instance | string | null | no |
| image_id | The image ID used for the instance | string | | yes |

## Outputs

| Name | Description |
|------|-------------|
| id | The ID of the ECS instance |
| private_ip | The private IP address of the instance |
```

#### 3.2.6 env_vars/{resource}.tfvars
```hcl
# Variables for alibabacloudstack_ecs_instance

# The image ID used for the instance
image_id = ""

# The type of instance to start
instance_type = ""

# The name of the ECS instance (Optional)
# instance_name = null
```

## 4. 配置和定制

### 4.1 配置文件支持
支持YAML配置文件来定制生成规则：
```yaml
# generate-config.yml
templates:
  base_dir: "templates/"
  
output:
  base_dir: "modules/alibabacloudstack/"
  example_dir: "example_alibabacloudstack/"
  
parsing:
  skip_deprecated: true
  include_examples: true
  
variable_defaults:
  string_default: null
  number_default: null
  bool_default: false
```

### 4.2 模板定制
支持Jinja2模板来定制生成的文件内容，提供默认模板并允许用户自定义。

## 5. 验证和测试

### 5.1 生成验证
- 验证生成的terraform语法正确性
- 检查变量引用的一致性
- 验证输出变量的有效性
- 确保modules和example目录下的README.md内容一致

### 5.2 测试策略
- 单元测试：测试解析函数
- 集成测试：测试完整的生成流程
- 回归测试：确保更新不破坏已有功能

## 6. 后续扩展

### 6.1 多语言支持
- 支持中文文档解析
- 支持双语README生成

### 6.2 CI/CD集成
- 支持GitHub Actions自动化
- 支持文档变更自动检测和模块更新

### 6.3 高级功能
- 支持模块依赖关系分析
- 支持terraform-docs自动生成
- 支持模块版本管理

## 7. 交付物

1. **核心脚本**: `generate-alibabacloudstack-modules.py`
2. **配置文件**: `config/module-generation.yml`
3. **模板文件**: `templates/` 目录
4. **文档**: 使用说明和开发文档
5. **测试用例**: 完整的测试套件

---

## 下一步行动
请确认以上PRD是否符合您的需求，如有需要调整的地方请告知。确认后我将开始开发核心脚本。
