#!/usr/bin/env python3
"""
Terraform模块自动生成工具
根据website/docs/r/目录下的文档自动生成terraform模块

用法:
  python generate-alibabacloudstack-modules.py --mode batch --input-dir website/docs/r/
  python generate-alibabacloudstack-modules.py --mode single --resource ecs_instance
"""

import os
import re
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentParser:
    """文档解析器"""

    def __init__(self):
        self.variable_types = {
            'string': 'string',
            'number': 'number',
            'bool': 'bool',
            'list': 'list(string)',
            'map': 'map(string)',
            'object': 'object({})'
        }

    def parse_resource_doc(self, file_path: str) -> Dict[str, Any]:
        """解析资源文档"""
        logger.info(f"解析文档: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取资源基本信息
        resource_info = self._extract_resource_info(content)

        # 提取参数信息
        arguments = self._extract_arguments(content)

        # 提取输出属性
        attributes = self._extract_attributes(content)

        # 提取示例代码
        examples = self._extract_examples(content)

        return {
            'resource_info': resource_info,
            'arguments': arguments,
            'attributes': attributes,
            'examples': examples
        }

    def _extract_resource_info(self, content: str) -> Dict[str, str]:
        """提取资源基本信息"""
        info = {}

        # 提取资源名称
        title_match = re.search(r'page_title:\s*"[^:]*:\s*([^"]+)"', content)
        if title_match:
            info['resource_name'] = title_match.group(1).strip()

        # 提取subcategory
        subcategory_match = re.search(r'subcategory:\s*"([^"]+)"', content)
        if subcategory_match:
            info['subcategory'] = subcategory_match.group(1).strip()

        # 提取description
        desc_match = re.search(r'description:\s*\|-?\s*\n\s*(.+)', content)
        if desc_match:
            info['description'] = desc_match.group(1).strip()

        return info

    def _extract_arguments(self, content: str) -> List[Dict[str, Any]]:
        """提取参数信息"""
        arguments = []

        # 查找Argument Reference部分
        arg_section_match = re.search(r'## Argument Reference\s*\n(.*?)(?=\n## |$)', content, re.DOTALL)
        if not arg_section_match:
            logger.warning("未找到Argument Reference部分")
            return arguments

        arg_content = arg_section_match.group(1)

        # 解析每个参数
        param_pattern = r'\* `([^`]+)` - \(([^)]+)\) (.+?)(?=\n\s*\* `|$)'
        param_matches = re.findall(param_pattern, arg_content, re.DOTALL)

        for param_name, param_flags, param_desc in param_matches:
            param_info = self._parse_parameter(param_name, param_flags, param_desc)
            arguments.append(param_info)

        return arguments

    def _parse_parameter(self, name: str, flags: str, description: str) -> Dict[str, Any]:
        """解析单个参数"""
        param = {
            'name': name,
            'description': description.strip().replace('\n', ' '),
            'required': 'Required' in flags,
            'force_new': 'ForceNew' in flags,
            'sensitive': 'Sensitive' in flags,
            'computed': 'Computed' in flags,
            'deprecated': 'Deprecated' in flags,
            'type': 'string',  # 默认类型
            'default': None
        }

        # 推断参数类型
        param['type'] = self._infer_parameter_type(description)

        # 提取默认值
        param['default'] = self._extract_default_value(description, param['type'])

        return param

    def _infer_parameter_type(self, description: str) -> str:
        """推断参数类型"""
        desc_lower = description.lower()

        # 布尔类型
        if re.search(r'\b(true|false)\b', desc_lower) or 'whether to' in desc_lower:
            return 'bool'

        # 数字类型
        if re.search(r'\b(number|size|count|port|bandwidth|timeout)\b', desc_lower):
            return 'number'

        # 列表类型
        if 'list of' in desc_lower or 'array of' in desc_lower or desc_lower.endswith('s'):
            if 'string' in desc_lower:
                return 'list(string)'
            elif 'number' in desc_lower:
                return 'list(number)'
            else:
                return 'list(string)'

        # Map类型
        if 'mapping' in desc_lower or 'map of' in desc_lower:
            return 'map(string)'

        # 对象类型
        if 'object' in desc_lower or 'block' in desc_lower:
            return 'any'

        return 'string'

    def _extract_default_value(self, description: str, param_type: str) -> Any:
        """从描述中提取默认值"""
        desc_lower = description.lower()

        # 查找 "Default is" 或 "Default:" 模式
        default_match = re.search(r'default\s+(?:is\s+)?[`"]?([^`".\n]+)[`"]?', desc_lower)
        if default_match:
            default_str = default_match.group(1).strip()

            # 根据类型转换默认值
            if param_type == 'bool':
                if default_str in ['true', 'false']:
                    return default_str == 'true'
            elif param_type == 'number':
                try:
                    return int(default_str) if default_str.isdigit() else float(default_str)
                except ValueError:
                    pass
            elif param_type == 'string':
                if default_str not in ['null', 'none', 'empty']:
                    return f'"{default_str}"'

        return None

    def _extract_attributes(self, content: str) -> List[Dict[str, str]]:
        """提取输出属性"""
        attributes = []

        # 查找Attributes Reference部分
        attr_section_match = re.search(r'## Attributes Reference\s*\n(.*?)(?=\n## |$)', content, re.DOTALL)
        if not attr_section_match:
            return attributes

        attr_content = attr_section_match.group(1)

        # 解析每个属性
        attr_pattern = r'\* `([^`]+)` - (.+?)(?=\n\s*\* `|$)'
        attr_matches = re.findall(attr_pattern, attr_content, re.DOTALL)

        for attr_name, attr_desc in attr_matches:
            attributes.append({
                'name': attr_name,
                'description': attr_desc.strip().replace('\n', ' ')
            })

        return attributes

    def _extract_examples(self, content: str) -> List[str]:
        """提取示例代码"""
        examples = []

        # 查找Example Usage部分的代码块
        example_pattern = r'## Example Usage.*?\n```hcl\n(.*?)\n```'
        example_matches = re.findall(example_pattern, content, re.DOTALL)

        for example in example_matches:
            examples.append(example.strip())

        return examples

class ModuleGenerator:
    """模块生成器"""

    def __init__(self, output_dir: str = "modules/alibabacloudstack", example_dir: str = "example_alibabacloudstack"):
        self.output_dir = Path(output_dir)
        self.example_dir = Path(example_dir)

    def generate_module(self, resource_data: Dict[str, Any], force: bool = False) -> bool:
        """生成terraform模块"""
        resource_name = resource_data['resource_info']['resource_name']

        # 解析资源名称
        name_parts = self._parse_resource_name(resource_name)
        if not name_parts:
            logger.error(f"无法解析资源名称: {resource_name}")
            return False

        service, resource = name_parts

        # 创建模块目录
        module_path = self.output_dir / service / f'{service}_{resource}'
        example_path = self.example_dir / service / f'{service}_{resource}'

        if module_path.exists() and not force:
            logger.warning(f"模块已存在: {module_path}")
            return False

        # 创建目录
        module_path.mkdir(parents=True, exist_ok=True)
        example_path.mkdir(parents=True, exist_ok=True)
        (example_path / "env_vars").mkdir(exist_ok=True)

        # 生成模块文件
        self._generate_main_tf(module_path, resource_data)
        self._generate_variables_tf(module_path, resource_data)
        self._generate_outputs_tf(module_path, resource_data)
        self._generate_versions_tf(module_path)

        # 生成示例文件
        self._generate_example_main_tf(example_path, service, resource, resource_data)
        self._generate_example_variables_tf(example_path, resource_data)
        self._generate_example_outputs_tf(example_path, resource_data)
        self._generate_example_versions_tf(example_path)
        self._generate_tfvars(example_path, resource_data)

        logger.info(f"成功生成模块: {module_path}")
        return True

    def _parse_resource_name(self, resource_name: str) -> Optional[Tuple[str, str]]:
        """解析资源名称，返回(service, resource)"""
        # 移除alibabacloudstack前缀
        if resource_name.startswith('alibabacloudstack_'):
            name = resource_name[18:]  # 移除'alibabacloudstack_'
        else:
            name = resource_name

        # 分割服务和资源名
        parts = name.split('_', 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return 'misc', name

    def _generate_main_tf(self, path: Path, resource_data: Dict[str, Any]):
        """生成main.tf"""
        resource_name = resource_data['resource_info']['resource_name']

        # 生成resource名称，如 "ecs_instance"
        if resource_name.startswith('alibabacloudstack_'):
            resource_local_name = resource_name[18:]  # 移除前缀
        else:
            resource_local_name = resource_name

        # 生成resource配置
        resource_config = f'resource "{resource_name}" "{resource_local_name}" {{\n'

        # 添加参数配置
        for arg in resource_data['arguments']:
            param_name = arg['name']

            if arg['type'] == 'any' or 'object' in arg['type']:
                # 对于复杂对象，使用dynamic块
                resource_config += f'  # {arg["description"]}\n'
                resource_config += f'  dynamic "{param_name}" {{\n'
                resource_config += f'    for_each = var.{param_name}\n'
                resource_config += f'    content {{\n'
                resource_config += f'      # 根据实际需要配置嵌套属性\n'
                resource_config += f'    }}\n'
                resource_config += f'  }}\n\n'
            else:
                # 普通参数
                resource_config += f'  # {arg["description"]}\n'
                resource_config += f'  {param_name} = var.{param_name}\n\n'

        resource_config += '}\n'

        with open(path / 'main.tf', 'w', encoding='utf-8') as f:
            f.write(resource_config)

    def _generate_variables_tf(self, path: Path, resource_data: Dict[str, Any]):
        """生成variables.tf"""
        variables_content = '# Variables for the module\n\n'

        for arg in resource_data['arguments']:
            variables_content += f'variable "{arg["name"]}" {{\n'
            variables_content += f'  type        = {arg["type"]}\n'
            variables_content += f'  description = "{arg["description"]}"\n'

            # 只有非必需参数且有默认值时才设置default
            if not arg['required'] and arg['default'] is not None:
                variables_content += f'  default     = {arg["default"]}\n'
            elif not arg['required']:
                variables_content += f'  default     = null\n'

            variables_content += '}\n\n'

        with open(path / 'variables.tf', 'w', encoding='utf-8') as f:
            f.write(variables_content)

    def _generate_outputs_tf(self, path: Path, resource_data: Dict[str, Any]):
        """生成outputs.tf"""
        resource_name = resource_data['resource_info']['resource_name']

        if resource_name.startswith('alibabacloudstack_'):
            resource_local_name = resource_name[18:]
        else:
            resource_local_name = resource_name

        outputs_content = '# Outputs for the module\n\n'

        # 默认输出ID
        outputs_content += f'output "id" {{\n'
        outputs_content += f'  description = "The ID of the {resource_local_name}"\n'
        outputs_content += f'  value       = {resource_name}.{resource_local_name}.id\n'
        outputs_content += '}\n\n'

        # 添加其他属性输出
        for attr in resource_data['attributes']:
            if attr['name'] != 'id':  # 避免重复
                outputs_content += f'output "{attr["name"]}" {{\n'
                outputs_content += f'  description = "{attr["description"]}"\n'
                outputs_content += f'  value       = {resource_name}.{resource_local_name}.{attr["name"]}\n'
                outputs_content += '}\n\n'

        with open(path / 'outputs.tf', 'w', encoding='utf-8') as f:
            f.write(outputs_content)

    def _generate_versions_tf(self, path: Path):
        """生成versions.tf"""
        versions_content = '''terraform {
  required_version = ">= 0.13"
  
  required_providers {
    alibabacloudstack = {
      source  = "aliyun/alibabacloudstack"
      version = ">= 3.16.0"
    }
  }
}
'''
        with open(path / 'versions.tf', 'w', encoding='utf-8') as f:
            f.write(versions_content)

    def _generate_example_main_tf(self, path: Path, service: str, resource: str, resource_data: Dict[str, Any]):
        """生成示例的main.tf"""
        module_path = f"../../../modules/alibabacloudstack/{service}/{service}_{resource}"

        main_content = f'''# Example usage of {service}_{resource} module

module "{service}_{resource}" {{
  source = "{module_path}"
  
'''

        # 添加所有变量引用
        for arg in resource_data['arguments']:
            main_content += f'  {arg["name"]} = var.{arg["name"]}\n'

        main_content += '}\n'

        with open(path / 'main.tf', 'w', encoding='utf-8') as f:
            f.write(main_content)

    def _generate_example_variables_tf(self, path: Path, resource_data: Dict[str, Any]):
        """生成示例的variables.tf"""
        # 直接复制模块的variables.tf
        self._generate_variables_tf(path, resource_data)

    def _generate_example_outputs_tf(self, path: Path, resource_data: Dict[str, Any]):
        """生成示例的outputs.tf"""
        resource_name = resource_data['resource_info']['resource_name']

        if resource_name.startswith('alibabacloudstack_'):
            resource_local_name = resource_name[18:]
        else:
            resource_local_name = resource_name

        outputs_content = f'''# Outputs from the {resource_local_name} module

output "id" {{
  description = "The ID of the {resource_local_name}"
  value       = module.{resource_local_name}.id
}}

'''

        # 添加其他输出
        for attr in resource_data['attributes']:
            if attr['name'] != 'id':
                outputs_content += f'output "{attr["name"]}" {{\n'
                outputs_content += f'  description = "{attr["description"]}"\n'
                outputs_content += f'  value       = module.{resource_local_name}.{attr["name"]}\n'
                outputs_content += '}\n\n'

        with open(path / 'outputs.tf', 'w', encoding='utf-8') as f:
            f.write(outputs_content)

    def _generate_example_versions_tf(self, path: Path):
        """生成示例的versions.tf"""
        self._generate_versions_tf(path)

    def _generate_tfvars(self, path: Path, resource_data: Dict[str, Any]):
        """生成tfvars文件"""
        resource_name = resource_data['resource_info']['resource_name']

        if resource_name.startswith('alibabacloudstack_'):
            filename = resource_name[18:] + '.tfvars'
        else:
            filename = resource_name + '.tfvars'

        tfvars_content = f'# Variables for {resource_name}\n\n'

        for arg in resource_data['arguments']:
            tfvars_content += f'# {arg["description"]}\n'

            if arg['required']:
                if arg['type'] == 'string':
                    tfvars_content += f'{arg["name"]} = ""\n\n'
                elif arg['type'] == 'number':
                    tfvars_content += f'{arg["name"]} = 0\n\n'
                elif arg['type'] == 'bool':
                    tfvars_content += f'{arg["name"]} = false\n\n'
                elif 'list' in arg['type']:
                    tfvars_content += f'{arg["name"]} = []\n\n'
                elif 'map' in arg['type'] or arg['type'] == 'any':
                    tfvars_content += f'{arg["name"]} = {{}}\n\n'
                else:
                    tfvars_content += f'# {arg["name"]} = ""\n\n'
            else:
                tfvars_content += f'# {arg["name"]} = null\n\n'

        with open(path / 'env_vars' / filename, 'w', encoding='utf-8') as f:
            f.write(tfvars_content)


def main():
    parser = argparse.ArgumentParser(description='生成AlibabaCloudStack Terraform模块')
    parser.add_argument('--mode', choices=['batch', 'single'], required=True,
                       help='生成模式：batch(批量) 或 single(单个)')
    parser.add_argument('--input-dir', default='website/docs/r/',
                       help='输入文档目录')
    parser.add_argument('--resource',
                       help='单个资源名称(single模式必需)')
    parser.add_argument('--output-dir', default='modules/alibabacloudstack',
                       help='模块输出目录')
    parser.add_argument('--example-dir', default='example_alibabacloudstack',
                       help='示例输出目录')
    parser.add_argument('--force', action='store_true',
                       help='强制覆盖已存在的模块')
    parser.add_argument('--verbose', action='store_true',
                       help='详细输出')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.mode == 'single' and not args.resource:
        logger.error("single模式需要指定--resource参数")
        sys.exit(1)

    parser_instance = DocumentParser()
    generator = ModuleGenerator(args.output_dir, args.example_dir)

    if args.mode == 'batch':
        # 批量处理
        input_path = Path(args.input_dir)
        if not input_path.exists():
            logger.error(f"输入目录不存在: {input_path}")
            sys.exit(1)

        success_count = 0
        total_count = 0

        for doc_file in input_path.glob('*.html.markdown'):
            total_count += 1
            try:
                resource_data = parser_instance.parse_resource_doc(str(doc_file))
                if generator.generate_module(resource_data, args.force):
                    success_count += 1
            except Exception as e:
                logger.error(f"处理文件 {doc_file} 失败: {e}")

        logger.info(f"批量处理完成: {success_count}/{total_count} 个模块生成成功")

    else:
        # 单个处理
        doc_file = Path(args.input_dir) / f"{args.resource}.html.markdown"
        if not doc_file.exists():
            logger.error(f"文档文件不存在: {doc_file}")
            sys.exit(1)

        try:
            resource_data = parser_instance.parse_resource_doc(str(doc_file))
            if generator.generate_module(resource_data, args.force):
                logger.info(f"模块生成成功: {args.resource}")
            else:
                logger.error(f"模块生成失败: {args.resource}")
        except Exception as e:
            logger.error(f"处理失败: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()
