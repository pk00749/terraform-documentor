# Terraform 模块开发指南

本文档介绍如何生成和维护 Terraform 模块的文档。

## 🚀 快速开始

### 环境要求

在开始之前，请确保已安装以下工具：

- **Python 3.6+**：用于运行文档生成脚本
- **terraform-docs**：用于生成 Terraform 文档
- **make**：用于执行便捷命令（可选）

### 安装依赖工具

```bash
# 检查并安装必要工具
make install
```

或者手动安装：

```bash
# 安装 terraform-docs (macOS)
brew install terraform-docs

# 安装 terraform-docs (Linux)
sudo apt-get update && sudo apt-get install -y terraform-docs
```

## 📋 文档生成方式

项目提供了多种文档生成方式：

### 1. 使用 Makefile（推荐）

```bash
# 生成英文版本文档
make docs

# 生成中文版本文档  
make docs-chinese

# 使用自定义配置生成文档
make docs-python CONFIG=path/to/config.yml

# 指定自定义模块目录
make docs-custom-dir MODULES_DIR=my-modules
```

### 2. 直接使用 Python 脚本

```bash
# 使用默认英文配置
python3 generate-docs.py

# 使用中文配置
python3 generate-docs.py --config config/chinese-docs.yml

# 指定自定义模块目录
python3 generate-docs.py --modules-dir custom-modules

# 查看所有选项
python3 generate-docs.py --help
```

## 🔧 配置文件说明

项目包含两个文档配置文件：

### 英文配置 - `.terraform-docs.yml`

- **位置**：项目根目录
- **特点**：标准英文文档格式
- **用途**：国际化项目或英文团队使用

### 中文配置 - `config/chinese-docs.yml`

- **位置**：config 目录
- **特点**：中文标题 + 表情符号装饰
- **用途**：中文团队或本地化项目使用

### 配置文件结构

```yaml
formatter: "markdown table"          # 输出格式
header-from: main.tf                # 标题来源文件
content: |-                         # 文档模板
  {{ .Header }}
  
  ## Important Notes              # 注意事项段落
  Please ensure that your Terraform environment is properly configured.
  
  {{ .Requirements }}             # 自动生成的各个段落
  {{ .Providers }}
  {{ .Resources }}
  {{ .Inputs }}
  {{ .Outputs }}

output:
  file: "README.md"               # 输出文件名
  mode: replace                   # 替换模式
```

## 📂 项目结构

```
terraform-documentor/
├── .terraform-docs.yml            # 英文配置文件
├── generate-docs.py               # Python 文��生成脚本
├── Makefile                      # 便捷命令定义
├── DEVELOPMENT.md                # 开发指南（本文件）
├── config/
│   └── chinese-docs.yml          # 中文配置文件
└── modules/
    ├── ec2/                      # EC2 模块
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   ├── versions.tf
    │   └── README.md             # 自动生成的文档
    ├── rds/                      # RDS 模块
    ├── s3/                       # S3 模块
    ├── security-group/           # 安全组模块
    └── vpc/                      # VPC 模块
```

## 🛠️ 常用开发命令

### 项目状态检查

```bash
# 检查所有模块和配置文件状态
make status
```

输出示例：
```
📊 模块状态检查...
🐍 Python 脚本: ✅ generate-docs.py
📋 英文配置: ✅ .terraform-docs.yml
📋 中文配置: ✅ config/chinese-docs.yml

📂 ec2:
  - main.tf: ✅
  - variables.tf: ✅
  - outputs.tf: ✅
  - versions.tf: ✅
  - README.md: ✅
```

### Terraform 代码维护

```bash
# 格式化 Terraform 代码
make fmt

# 验证 Terraform 语法
make validate
```

### 文档重新生成

```bash
# 重新生成所有文档
make regenerate

# 查看帮助信息
make help
```

## 📝 添加新模块

当添加新的 Terraform 模块时，请按照以下步骤：

### 1. 创建模块目录结构

```bash
mkdir -p modules/new-module
cd modules/new-module
```

### 2. 创建必要的 Terraform 文件

```bash
# 主要资源定义
touch main.tf

# 输入变量定义
touch variables.tf

# 输出值定义
touch outputs.tf

# 版本约束定义
touch versions.tf
```

### 3. 在 main.tf 中添加模块描述

```hcl
# 新模块名称
# 模块功能的简要描述

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# 在这里定义你的资源
```

### 4. 生成文档

```bash
# 返回项目根���录
cd ../..

# 生成文档
make docs
```

新模块将自动被检测到并生成相应的 README.md 文档。

## 🎯 文档内容说明

生成的文档包含以下段落：

### 英文版本文档结构

1. **模块标题**：从 main.tf 的注释自动提取
2. **Important Notes**：使用前的重要提醒
3. **Requirements**：Terraform 版本要求
4. **Providers**：所需的 Provider 信息
5. **Modules**：子模块信息
6. **Resources**：创建的资源列表
7. **Inputs**：输入变量表格
8. **Outputs**：输出值表格

### 中文版本文档结构

1. **模块标题**：从 main.tf 的注释自动提取
2. **📋 模块概述**：模块功能说明
3. **⚠️ 注意事项**：使用前的重要提醒
4. **⚙️ 技术要求**：Terraform 版本要求
5. **🔌 提供商配置**：所需的 Provider 信息
6. **📦 子模块**：子模块信息
7. **🏗️ 资源清单**：创建的资源列表
8. **📥 输入参数**：输入变量表格
9. **📤 输出结果**：输出值表格
10. **🚀 使用示例**：HCL 代码示例

## 🚨 故障排除

### 常见问题及解决方案

**1. terraform-docs 未找到**
```bash
# 解决方案：安装 terraform-docs
brew install terraform-docs
```

**2. Python 脚本执行权限不足**
```bash
# 解决方案：添加执行权限
chmod +x generate-docs.py
```

**3. 模块未被检测到**
- 确保模块目录下包含 `.tf` 文件
- 检查目录结构是否正确
- 运行 `make status` 查看模块状态

**4. 文档格式不正确**
- 检查配置文件语法是否正确
- 确认 main.tf 文件包含模块描述注释
- 重新生成文档：`make regenerate`

## 📚 进阶配置

### 自定义文档配置

如需创建自定义配置文件：

1. 复制现有配置文件
```bash
cp .terraform-docs.yml config/custom-docs.yml
```

2. 修改配置内容

3. 使用自定义配置生成文档
```bash
make docs-python CONFIG=config/custom-docs.yml
```

### 批量操作

```bash
# 格式化所有 Terraform 文件
terraform fmt -recursive .

# 验证所有模块
find modules -name "*.tf" -execdir terraform validate \;

# 清理所有生成的文档
find modules -name "README.md" -delete
```

## 🔄 CI/CD 集成

在 CI/CD 流水线中使用：

```yaml
# GitHub Actions 示例
- name: Generate Terraform Docs
  run: |
    pip3 install --upgrade pip
    python3 generate-docs.py
    
- name: Check for changes
  run: |
    git diff --exit-code || echo "Documentation updated"
```

## 📞 获取帮助

- 查看 Makefile 帮助：`make help`
- 查看 Python 脚本帮助：`python3 generate-docs.py --help`
- 检查项目状态：`make status`

---

最后更新：2025-07-23
