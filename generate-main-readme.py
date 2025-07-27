#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主目录 README.md 生成脚本
基于 terraform-docs 提取模块信息，生成项目主目录的 README.md
支持中英文双语生成
"""

import os
import sys
import subprocess
import json
from datetime import datetime


class Colors:
    """终端颜色类"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class MainReadmeGenerator:
    """主目录 README.md 生成器"""

    def __init__(self, modules_dir="example_alibabacloudstack", output_file="README.md"):
        self.modules_dir = modules_dir
        self.output_file = output_file
        self.project_info = {
            "name": "Terraform Share Modules",
            "description": "这个项目提供了一套全面的 Terraform 模块文档生成系统。支持中英文文档生成以及集中化配置管理。",
            "description_en": "This project provides a comprehensive documentation generation system for Terraform modules. It supports both English and Chinese documentation generation with centralized configuration management."
        }

    def print_colored(self, message, color=Colors.ENDC):
        """打印彩色消息"""
        print(f"{color}{message}{Colors.ENDC}")

    def print_emoji(self, emoji, message, color=Colors.ENDC):
        """打印带表情符号的消息"""
        print(f"{color}{emoji} {message}{Colors.ENDC}")

    def check_terraform_docs_installed(self):
        """检查 terraform-docs 是否已安装"""
        try:
            result = subprocess.run(['terraform-docs', '--version'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except FileNotFoundError:
            pass
        return False

    def get_module_info(self, module_path):
        """提取单个模块的信息"""
        module_name = os.path.basename(module_path)

        # 检查是否有 main.tf 文件
        main_tf_path = os.path.join(module_path, "main.tf")
        if not os.path.exists(main_tf_path):
            return None

        module_info = {
            "name": module_name,
            "path": module_path,
            "description": "",
            "description_en": "",
            "version": "",
            "providers": [],
            "inputs_count": 0,
            "outputs_count": 0,
            "resources_count": 0
        }

        try:
            # 使用 terraform-docs 提取模块信息
            result = subprocess.run([
                'terraform-docs',
                'json',
                module_path
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                data = json.loads(result.stdout)

                # 提取描述信息
                if 'header' in data and data['header']:
                    # 从 header 中提取描述
                    header_lines = data['header'].strip().split('\n')
                    for line in header_lines:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if not module_info['description']:
                                module_info['description'] = line
                            break

                # 提取统计信息
                module_info['inputs_count'] = len(data.get('inputs', []))
                module_info['outputs_count'] = len(data.get('outputs', []))
                module_info['resources_count'] = len(data.get('resources', []))

                # 提取 providers 信息
                providers = data.get('providers', [])
                for provider in providers:
                    module_info['providers'].append(provider.get('name', ''))

                # 提取版本要求
                requirements = data.get('requirements', [])
                for req in requirements:
                    if req.get('name') == 'terraform':
                        module_info['version'] = req.get('version', '')

        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
            self.print_emoji("⚠️", f"无法提取 {module_name} 的详细信息: {str(e)}", Colors.WARNING)

        # 从 main.tf 文件中读取注释作为描述
        try:
            with open(main_tf_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                description_lines = []

                for line in lines[:10]:  # 只检查前10行
                    line = line.strip()
                    if line.startswith('#') and not line.startswith('##'):
                        desc = line.lstrip('#').strip()
                        if desc and '模块' in desc:
                            description_lines.append(desc)

                if description_lines:
                    module_info['description'] = description_lines[0]

        except Exception as e:
            pass

        # 设置默认描述
        if not module_info['description']:
            module_info['description'] = f"{module_name.upper()} 模块"

        # 设置英文描述
        module_descriptions = {
            'ec2': 'AWS EC2 instance management with configurable settings',
            'rds': 'AWS RDS database instances with backup and monitoring',
            's3': 'AWS S3 bucket configuration with security policies',
            'security-group': 'AWS Security Group rules and configurations',
            'vpc': 'AWS VPC networking with subnets and routing'
        }
        module_info['description_en'] = module_descriptions.get(module_name, f"{module_name.upper()} module")

        return module_info

    def get_all_modules_info(self):
        """获取所有模块的信息"""
        modules_info = []

        if not os.path.exists(self.modules_dir):
            self.print_emoji("❌", f"模块目录 {self.modules_dir} 不存在", Colors.FAIL)
            return modules_info

        # 递归遍历模块目录
        self.print_emoji("🔍", f"开始扫描目录: {self.modules_dir}", Colors.OKCYAN)
        modules_info = self._scan_directory_recursively(self.modules_dir)

        return sorted(modules_info, key=lambda x: x['name'])

    def _scan_directory_recursively(self, directory, base_path=""):
        """递归扫描目录寻找Terraform模块"""
        modules_info = []

        try:
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)

                # 跳过隐藏文件和特殊目录
                if item.startswith('.') or item == '__pycache__' or item == 'env_vars':
                    continue

                if os.path.isdir(item_path):
                    # 检查当前目录是否是一个Terraform模块
                    if self._is_terraform_module(item_path):
                        # 构建模块的相对路径名称
                        if base_path:
                            module_name = f"{base_path}/{item}"
                        else:
                            module_name = item

                        self.print_emoji("📂", f"发现模块: {module_name}", Colors.OKBLUE)
                        module_info = self.get_module_info(item_path)
                        if module_info:
                            # 更新模块名称为包含路径的名称
                            module_info['name'] = module_name
                            module_info['relative_path'] = module_name
                            modules_info.append(module_info)
                    else:
                        # 如果不是模块，继续递归扫描子目录
                        new_base_path = f"{base_path}/{item}" if base_path else item
                        sub_modules = self._scan_directory_recursively(item_path, new_base_path)
                        modules_info.extend(sub_modules)

        except PermissionError:
            self.print_emoji("⚠️", f"无权限访问目录: {directory}", Colors.WARNING)
        except Exception as e:
            self.print_emoji("⚠️", f"扫描目录时出错 {directory}: {str(e)}", Colors.WARNING)

        return modules_info

    def _is_terraform_module(self, directory):
        """检查目录是否是一个Terraform模块"""
        # 检查是否有必要的Terraform文件
        tf_files = ['main.tf', 'variables.tf', 'outputs.tf']
        for tf_file in tf_files:
            if os.path.exists(os.path.join(directory, tf_file)):
                return True

        # 也检查是否有任何.tf文件
        try:
            for item in os.listdir(directory):
                if item.endswith('.tf'):
                    return True
        except (PermissionError, OSError):
            pass

        return False

    def generate_module_table_cn(self, modules_info):
        """生成中文模块表格"""
        if not modules_info:
            return "暂无可用模块。"

        table = "| 模块名称 | 描述 | 输入参数 | 输出参数 | 资源数量 | 状态 |\n"
        table += "|--------|------|----------|----------|----------|------|\n"

        for module in modules_info:
            status = "✅ 可用"
            table += f"| [{module['name']}]({self.modules_dir}/{module['name']}/) | {module['description']} | {module['inputs_count']} | {module['outputs_count']} | {module['resources_count']} | {status} |\n"

        return table

    def generate_module_table_en(self, modules_info):
        """生成英文模块表格"""
        if not modules_info:
            return "No modules available."

        table = "| Module | Description | Inputs | Outputs | Resources | Status |\n"
        table += "|--------|-------------|---------|---------|-----------|--------|\n"

        for module in modules_info:
            status = "✅ Active"
            table += f"| [{module['name']}]({self.modules_dir}/{module['name']}/) | {module['description_en']} | {module['inputs_count']} | {module['outputs_count']} | {module['resources_count']} | {status} |\n"

        return table

    def generate_readme_content(self, modules_info, language='both'):
        """生成 README 内容"""
        current_date = datetime.now().strftime("%Y-%m-%d")

        if language == 'cn':
            return self.generate_chinese_readme(modules_info, current_date)
        elif language == 'en':
            return self.generate_english_readme(modules_info, current_date)
        else:
            return self.generate_bilingual_readme(modules_info, current_date)

    def generate_chinese_readme(self, modules_info, current_date):
        """生成中文 README"""
        module_table = self.generate_module_table_cn(modules_info)

        content = f"""# Terraform 模块文档项目

本项目包含以下 Terraform 模块：

## 可用模块

{module_table}

---

**最后更新**: {current_date}
"""
        return content

    def generate_english_readme(self, modules_info, current_date):
        """生成英文 README"""
        module_table = self.generate_module_table_en(modules_info)

        content = f"""# Terraform Share Modules

This project contains the following Terraform modules:

## Available Modules

{module_table}

---

**Last Updated**: {current_date}
"""
        return content

    def generate_bilingual_readme(self, modules_info, current_date):
        """生成双语 README"""
        module_table_cn = self.generate_module_table_cn(modules_info)
        module_table_en = self.generate_module_table_en(modules_info)

        content = f"""# Terraform Modules Documentation Project / Terraform 模块文档项目

## Available Modules / 可用模块

**English**:
{module_table_en}

**中文**:
{module_table_cn}

---

**Last Updated / 最后更新**: {current_date}
"""
        return content

    def run(self, language='both'):
        """运行主程序"""
        self.print_emoji("🚀", "开始生成主目录 README.md", Colors.HEADER)

        # 检查 terraform-docs
        if not self.check_terraform_docs_installed():
            self.print_emoji("❌", "terraform-docs 未安装，请先安装 terraform-docs", Colors.FAIL)
            return False

        # 获取模块信息
        self.print_emoji("📂", "扫描模块目录...", Colors.OKBLUE)
        modules_info = self.get_all_modules_info()

        if not modules_info:
            self.print_emoji("⚠️", "未找到任何可用模块", Colors.WARNING)
            return False

        self.print_emoji("✅", f"找到 {len(modules_info)} 个模块", Colors.OKGREEN)

        # 生成 README 内容
        self.print_emoji("📝", f"生成 README 内容 (语言: {language})...", Colors.OKBLUE)
        readme_content = self.generate_readme_content(modules_info, language)

        # 写入文件
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            self.print_emoji("✅", f"README.md 生成成功: {self.output_file}", Colors.OKGREEN)
            return True
        except Exception as e:
            self.print_emoji("❌", f"写入文件失败: {str(e)}", Colors.FAIL)
            return False


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='生成主目录 README.md')
    parser.add_argument('--lang', choices=['cn', 'en', 'both'], default='en',
                       help='生成语言版本 (cn: 中文, en: 英文, both: 双语)')
    parser.add_argument('--modules-dir', default='example_alibabacloudstack',
                       help='模块目录路径 (默认: example_alibabacloudstack)')
    parser.add_argument('--output', default='README.md',
                       help='输出文件名 (默认: README.md)')

    args = parser.parse_args()

    generator = MainReadmeGenerator(args.modules_dir, args.output)
    success = generator.run(args.lang)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
