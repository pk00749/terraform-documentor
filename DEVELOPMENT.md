# Terraform 模块开发指南

## 快速开始

1. **安装依赖工具**：
   ```bash
   make install-deps
   ```

2. **生成文档**：
   ```bash
   make docs          # 基础文档
   make docs-advanced # 带图标和架构图的高级文档
   ```

3. **开发流程**：
   ```bash
   make all          # 完整开发流程
   make ci           # CI/CD 流程
   ```

## 文档生成选项

### 使用 terraform-docs 直接生成
```bash
# 基础文档生成
terraform-docs .

# 使用自定义配置
terraform-docs --config .terraform-docs-advanced.yml .

# 生成不同格式
terraform-docs markdown table .
terraform-docs json .
terraform-docs yaml .
```

### 使用提供的脚本
```bash
# 自动化脚本
./generate-docs.sh

# Makefile 命令
make docs           # 基础文档
make docs-advanced  # 高级文档
make help          # 查看所有可用命令
```

## 配置文件说明

- `.terraform-docs.yml` - 基础配置
- `.terraform-docs-advanced.yml` - 包含图标、架构图的高级配置
- `.github/workflows/terraform-docs.yml` - GitHub Actions 自动化
- `Makefile` - 开发任务自动化

## 自动化集成

### GitHub Actions
配置的工作流程会在每次推送或 PR 时自动：
- 生成最新文档
- 验证 Terraform 格式
- 提交文档更新

### Pre-commit Hook
建议添加 pre-commit 配置来确保代码质量：

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/terraform-docs/terraform-docs
    rev: v0.16.0
    hooks:
      - id: terraform-docs-go
        args: ['markdown', 'table', '--output-file', 'README.md', '.']
```
