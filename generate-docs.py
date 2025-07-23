#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Terraform 文档生成脚本 (Python版本)
使用 terraform-docs 工具遍历多个模块
只使用 Python 标准库，无需额外安装依赖
"""

import os
import sys
import subprocess
import argparse
import glob
from pathlib import Path
import re


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


class TerraformDocsGenerator:
    """Terraform 文档生成器"""

    def __init__(self, modules_dir="modules", config_file=".terraform-docs.yml"):
        self.modules_dir = modules_dir
        self.config_file = config_file
        self.total_modules = 0
        self.successful_modules = 0
        self.failed_modules = 0

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

    def install_terraform_docs(self):
        """尝试安装 terraform-docs"""
        self.print_emoji("❌", "terraform-docs 未安装，正在尝试安装...", Colors.WARNING)

        # 检查是否有 brew
        try:
            subprocess.run(['brew', '--version'], capture_output=True, check=True)
            self.print_emoji("📦", "使用 Homebrew 安装 terraform-docs...")
            result = subprocess.run(['brew', 'install', 'terraform-docs'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.print_emoji("✅", "terraform-docs 安装成功", Colors.OKGREEN)
                return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        # 检查是否有 apt-get
        try:
            subprocess.run(['apt-get', '--version'], capture_output=True, check=True)
            self.print_emoji("📦", "使用 apt-get 安装 terraform-docs...")
            result = subprocess.run(['sudo', 'apt-get', 'update'], capture_output=True)
            if result.returncode == 0:
                result = subprocess.run(['sudo', 'apt-get', 'install', '-y', 'terraform-docs'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.print_emoji("✅", "terraform-docs 安装成功", Colors.OKGREEN)
                    return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        self.print_emoji("❌", "无法自动安装 terraform-docs，请手动安装", Colors.FAIL)
        return False

    def check_config_file_exists(self):
        """检查全局配置文件是否存在"""
        if not os.path.isfile(self.config_file):
            self.print_emoji("❌", f"全局配置文件 {self.config_file} 不存在", Colors.FAIL)
            return False
        return True

    def has_terraform_files(self, directory):
        """检查目录是否包含 Terraform 文件"""
        tf_files = glob.glob(os.path.join(directory, "*.tf"))
        return len(tf_files) > 0

    def clean_local_configs(self):
        """清理模块中的本地配置文件"""
        self.print_emoji("🧹", "清理模块中的本地配置文件...")

        if not os.path.exists(self.modules_dir):
            return

        config_files = glob.glob(os.path.join(self.modules_dir, "**", ".terraform-docs.yml"),
                               recursive=True)

        for config_file in config_files:
            try:
                os.remove(config_file)
            except OSError:
                pass

        self.print_emoji("✅", "本地配置文件清理完成", Colors.OKGREEN)

    def remove_duplicate_headers(self, readme_path):
        """移除文档中的重复标题"""
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 移除重复的标题，保留带emoji的版本
            patterns_to_remove = [
                r'\n## Requirements\n',
                r'\n## Providers\n',
                r'\n## Modules\n',
                r'\n## Resources\n',
                r'\n## Inputs\n',
                r'\n## Outputs\n'
            ]

            for pattern in patterns_to_remove:
                content = re.sub(pattern, '\n', content)

            # 写回文件
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except Exception as e:
            # 如果后处理失败，不影响主要功能
            pass

    def generate_module_docs(self, module_path):
        """为单个模块生成文档"""
        module_name = os.path.basename(module_path)
        self.print_emoji("📂", f"处理模块: {module_name}", Colors.OKBLUE)

        # 检查是否有 Terraform 文件
        if not self.has_terraform_files(module_path):
            self.print_emoji("⚠️", f"{module_path} 中没有找到 Terraform 文件，跳过", Colors.WARNING)
            return True

        # 生成文档
        self.print_emoji("📝", f"为 {module_name} 生成文档...")

        try:
            result = subprocess.run([
                'terraform-docs',
                '--config', self.config_file,
                module_path
            ], capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                # 后处理：移除重复标题
                readme_path = os.path.join(module_path, 'README.md')
                if os.path.exists(readme_path):
                    self.remove_duplicate_headers(readme_path)

                self.print_emoji("✅", f"{module_name} 文档生成成功", Colors.OKGREEN)
                return True
            else:
                self.print_emoji("❌", f"{module_name} 文档生成失败", Colors.FAIL)
                if result.stderr:
                    print(f"错误信息: {result.stderr.strip()}")
                return False

        except subprocess.TimeoutExpired:
            self.print_emoji("❌", f"{module_name} 文档生成超时", Colors.FAIL)
            return False
        except Exception as e:
            self.print_emoji("❌", f"{module_name} 文档生成异常: {str(e)}", Colors.FAIL)
            return False

    def process_root_directory(self):
        """处理根目录（如果有 Terraform 文件）"""
        if self.has_terraform_files("."):
            self.print_emoji("📂", "处理根目录", Colors.OKBLUE)
            self.total_modules += 1

            try:
                result = subprocess.run([
                    'terraform-docs',
                    '--config', self.config_file,
                    '.'
                ], capture_output=True, text=True, timeout=60)

                if result.returncode == 0:
                    self.print_emoji("✅", "根目录文档生成成功", Colors.OKGREEN)
                    self.successful_modules += 1
                else:
                    self.print_emoji("❌", "根目录文档生成失败", Colors.FAIL)
                    self.failed_modules += 1

            except Exception as e:
                self.print_emoji("❌", f"根目录文档生成异常: {str(e)}", Colors.FAIL)
                self.failed_modules += 1

    def scan_modules(self):
        """扫描并处理所有模块"""
        if not os.path.exists(self.modules_dir):
            self.print_emoji("❌", f"模块目录 '{self.modules_dir}' 不存在", Colors.FAIL)
            return False

        self.print_emoji("🔍", f"扫描模块目录: {self.modules_dir}", Colors.OKCYAN)
        self.print_emoji("📋", f"使用全局配置文件: {self.config_file}", Colors.OKCYAN)

        # 获取所有模块目录
        module_dirs = [d for d in glob.glob(os.path.join(self.modules_dir, "*"))
                      if os.path.isdir(d)]

        if not module_dirs:
            self.print_emoji("⚠️", f"在 {self.modules_dir} 中未找到任何模块目录", Colors.WARNING)
            return True

        # 处理每个模块
        for module_dir in sorted(module_dirs):
            self.total_modules += 1

            if self.generate_module_docs(module_dir):
                self.successful_modules += 1
            else:
                self.failed_modules += 1

            print()  # 添加空行分隔

        return True

    def print_statistics(self):
        """输出统计结果"""
        print("=" * 20)
        self.print_emoji("📊", "生成结果统计:", Colors.HEADER)
        print(f"   总模块数: {self.total_modules}")
        print(f"   成功: {self.successful_modules}")
        print(f"   失败: {self.failed_modules}")
        print(f"   配置文件: {self.config_file}")
        print("=" * 20)

        if self.failed_modules == 0:
            self.print_emoji("🎉", "所有文档生成完成！", Colors.OKGREEN)
            return True
        else:
            self.print_emoji("⚠️", "部分模块文档生成失败，请检查错误信息", Colors.WARNING)
            return False

    def run(self):
        """主执行函数"""
        self.print_emoji("🚀", "开始生成 Terraform 文档...", Colors.HEADER)

        # 检查 terraform-docs 是否安装
        if not self.check_terraform_docs_installed():
            if not self.install_terraform_docs():
                sys.exit(1)

        # 检查配置文件是否存在
        if not self.check_config_file_exists():
            sys.exit(1)

        # 清理本地配置文件
        self.clean_local_configs()

        # 扫描并处理模块
        if not self.scan_modules():
            sys.exit(1)

        # 处理根目录
        self.process_root_directory()

        # 输出统计结果
        success = self.print_statistics()

        sys.exit(0 if success else 1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Terraform 文档生成脚本 (Python版本)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 generate-docs.py                              # 使用默认配置
  python3 generate-docs.py --config config/chinese-docs.yml  # 使用中文配置
  python3 generate-docs.py --modules-dir my-modules     # 指定模块目录
        """
    )

    parser.add_argument(
        '--config',
        default='.terraform-docs.yml',
        help='指定配置文件路径 (默认: .terraform-docs.yml)'
    )

    parser.add_argument(
        '--modules-dir',
        default='modules',
        help='指定模块目录 (默认: modules)'
    )

    args = parser.parse_args()

    # 创建生成器实例并运行
    generator = TerraformDocsGenerator(
        modules_dir=args.modules_dir,
        config_file=args.config
    )

    generator.run()


if __name__ == "__main__":
    main()
