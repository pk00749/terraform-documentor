#!/usr/bin/env python3
# 测试同步功能

import os
import sys
import shutil

def test_sync():
    print("🚀 开始测试同步功能...")

    modules_dir = "modules/alibabacloudstack/adb/adb_account"
    example_dir = "example_alibabacloudstack"

    print(f"📂 模块目录: {modules_dir}")
    print(f"📂 示例目录: {example_dir}")

    # 检查目录是否存在
    print(f"模块目录存在: {os.path.exists(modules_dir)}")
    print(f"示例目录存在: {os.path.exists(example_dir)}")

    if os.path.exists(modules_dir):
        # 检查是否有 Terraform 文件
        tf_files = [f for f in os.listdir(modules_dir) if f.endswith('.tf')]
        print(f"Terraform 文件: {tf_files}")

        # 检查是否有 README.md
        readme_exists = os.path.exists(os.path.join(modules_dir, 'README.md'))
        print(f"README.md 存在: {readme_exists}")

    # 计算相对路径
    if 'modules/alibabacloudstack' in modules_dir:
        rel_path = modules_dir.split('modules/alibabacloudstack/')[-1]
        example_path = os.path.join(example_dir, rel_path)
        print(f"📍 相对路径: {rel_path}")
        print(f"📍 目标示例路径: {example_path}")
        print(f"目标示例路径存在: {os.path.exists(example_path)}")

        # 尝试同步
        if os.path.exists(modules_dir) and os.path.exists(example_path):
            modules_readme = os.path.join(modules_dir, 'README.md')
            example_readme = os.path.join(example_path, 'README.md')

            if os.path.exists(modules_readme):
                try:
                    shutil.copy2(modules_readme, example_readme)
                    print(f"✅ 成功同步 README.md 到 {example_path}")
                    return True
                except Exception as e:
                    print(f"❌ 同步失败: {e}")
                    return False
            else:
                print(f"⚠️ 源 README.md 不存在: {modules_readme}")
        else:
            print("⚠️ 源目录或目标目录不存在")

    return False

if __name__ == "__main__":
    test_sync()
