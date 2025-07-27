.PHONY: docs docs-python docs-chinese install clean help status validate fmt regenerate

# 默认目标
all: docs

# 生成所有模块的文档（使用Python脚本和英文配置）
docs:
	@echo "🚀 生成 Terraform 文档（英文版本）..."
	@python3 generate-docs.py --config config/english-docs.yml

# 使用Python脚本生成文档（可自定义配置）
docs-python:
	@echo "🚀 使用 Python 脚本生成 Terraform 文档..."
	@if [ -n "$(CONFIG)" ]; then \
		python3 generate-docs.py --config $(CONFIG); \
	else \
		python3 generate-docs.py; \
	fi

# 生成中文文档
docs-chinese:
	@echo "🚀 生成 Terraform 文档（中文版本）..."
	@python3 generate-docs.py --config config/chinese-docs.yml

# 使用自定义模块目录生成文档
docs-custom-dir:
	@echo "🚀 使用自定义模块目录生成文档..."
	@if [ -n "$(MODULES_DIR)" ]; then \
		if [ -n "$(CONFIG)" ]; then \
			python3 generate-docs.py --modules-dir $(MODULES_DIR) --config $(CONFIG); \
		else \
			python3 generate-docs.py --modules-dir $(MODULES_DIR) --config config/english-docs.yml; \
		fi \
	else \
		echo "❌ 请使用 make docs-custom-dir MODULES_DIR=path/to/modules [CONFIG=config/file.yml]"; \
	fi

# 安装 terraform-docs
install:
	@echo "📦 检查并安装必要工具..."
	@echo "🐍 检查 Python 3..."
	@python3 --version || (echo "❌ 请先安装 Python 3"; exit 1)
	@echo "📋 检查 terraform-docs..."
	@if ! command -v terraform-docs >/dev/null 2>&1; then \
		echo "📦 安装 terraform-docs..."; \
		if command -v brew >/dev/null 2>&1; then \
			brew install terraform-docs; \
		else \
			echo "❌ 请先安装 Homebrew 或手动安装 terraform-docs"; \
			exit 1; \
		fi; \
	else \
		echo "✅ terraform-docs 已安装"; \
	fi

# 清理生成的文件
clean:
	@echo "🧹 清理生成的文件..."
	@echo "ℹ️  Python 脚本专注于文档生成，如需清理可手动删除 README.md 文件"
	@echo "💡 使用: find modules -name 'README.md' -delete"

# 强制重新生成所有文档
regenerate: docs
	@echo "🔄 重新生成完成"

# 检查模块状态
status:
	@echo "📊 模块状态检查..."
	@echo "🐍 Python 脚本: $$([ -f "generate-docs.py" ] && echo "✅ generate-docs.py" || echo "❌ generate-docs.py 不存在")"
	@echo "📋 英文配置: $$([ -f "config/english-docs.yml" ] && echo "✅ config/english-docs.yml" || echo "❌ config/english-docs.yml 不存在")"
	@echo "📋 中文配置: $$([ -f "config/chinese-docs.yml" ] && echo "✅ config/chinese-docs.yml" || echo "❌ config/chinese-docs.yml 不存在")"
	@echo ""
	@for dir in modules/*/; do \
		if [ -d "$$dir" ]; then \
			module_name=$$(basename "$$dir"); \
			echo "📂 $$module_name:"; \
			echo "  - main.tf: $$([ -f "$$dir/main.tf" ] && echo "✅" || echo "❌")"; \
			echo "  - variables.tf: $$([ -f "$$dir/variables.tf" ] && echo "✅" || echo "❌")"; \
			echo "  - outputs.tf: $$([ -f "$$dir/outputs.tf" ] && echo "✅" || echo "❌")"; \
			echo "  - versions.tf: $$([ -f "$$dir/versions.tf" ] && echo "✅" || echo "❌")"; \
			echo "  - README.md: $$([ -f "$$dir/README.md" ] && echo "✅" || echo "❌")"; \
			echo ""; \
		fi \
	done

# 验证 Terraform 语法
validate:
	@echo "🔍 验证 Terraform 语法..."
	@for dir in modules/*/; do \
		if [ -d "$$dir" ] && [ -f "$$dir/main.tf" ]; then \
			echo "检查 $$(basename "$$dir")..."; \
			(cd "$$dir" && terraform fmt -check=true -diff=true) || exit 1; \
			(cd "$$dir" && terraform validate) || exit 1; \
		fi \
	done
	@echo "✅ 所有模块语法验证通过"

# 格式化 Terraform 代码
fmt:
	@echo "🎨 格式化 Terraform 代码..."
	@terraform fmt -recursive .
	@echo "✅ 代码格式化完成"

# 显示帮助信息
help:
	@echo "Terraform 文档生成器 (Python 版本)"
	@echo ""
	@echo "🐍 基于 Python 脚本的文档生成工具"
	@echo ""
	@echo "📋 可用命令:"
	@echo "  make docs                     - 生成英文版本文档"
	@echo "  make docs-chinese             - 生成中文版本文档"
	@echo "  make docs-python CONFIG=path - 使用指定配置生成文档"
	@echo "  make docs-custom-dir MODULES_DIR=path - 使用自定义模块目录"
	@echo "  make install                  - 检查并安装必要工具"
	@echo "  make clean                    - 查看清理说明"
	@echo "  make regenerate               - 重新生成所有文档"
	@echo "  make status                   - 检查项目和模块状态"
	@echo "  make validate                 - 验证 Terraform 语法"
	@echo "  make fmt                      - 格式化 Terraform 代码"
	@echo "  make help                     - 显示此帮助信息"
	@echo ""
	@echo "🌟 使用示例:"
	@echo "  make docs                                    # 生成英文文档"
	@echo "  make docs-chinese                            # 生成中文文档"
	@echo "  make docs-python CONFIG=config/custom.yml   # 使用自定义配置"
	@echo "  make docs-custom-dir MODULES_DIR=my-modules  # 指定模块目录"
	@echo ""
	@echo "💡 配置文件:"
	@echo "  📄 config/english-docs.yml   - 英文配置"
	@echo "  📄 config/chinese-docs.yml   - 中文配置"
