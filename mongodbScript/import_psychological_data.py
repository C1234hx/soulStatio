#!/usr/bin/env python3
"""
心理知识数据导入脚本
用于将JSON格式的心理知识数据导入到MongoDB数据库中
"""

import os
import sys
import json
import argparse

# 将项目根目录添加到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入Django设置
import django
django.setup()

# 导入心理知识模型
from api.models import PsychologicalKnowledge, PsychologicalKnowledgeChild


def import_psychological_data(json_file_path):
    """
    导入心理知识数据到MongoDB
    
    Args:
        json_file_path: JSON数据文件的路径
    """
    try:
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"成功读取JSON文件: {json_file_path}")
        print(f"数据总量: {len(data)}")
        
        # 遍历数据，递归创建心理知识分类
        for item in data:
            # 递归创建子分类
            childrens = []
            if 'childrens' in item and item['childrens']:
                childrens = create_childrens(item['childrens'])
            
            # 创建主分类
            knowledge = PsychologicalKnowledge(
                id=item['id'],
                content=item['content'],
                childrens=childrens
            )
            knowledge.save()
            print(f"成功导入: {item['content']}")
        
        print("\n✅ 数据导入完成!")
        print(f"共导入 {len(data)} 条心理知识数据")
        
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 {json_file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ 错误: 无法解析JSON文件 {json_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: 导入失败 - {str(e)}")
        sys.exit(1)


def create_childrens(childrens_data):
    """
    递归创建子分类
    
    Args:
        childrens_data: 子分类数据列表
        
    Returns:
        创建好的子分类对象列表
    """
    childrens = []
    
    for child_data in childrens_data:
        # 递归处理更深层次的子分类
        grandchildrens = []
        if 'childrens' in child_data and child_data['childrens']:
            grandchildrens = create_childrens(child_data['childrens'])
        
        # 创建子分类对象
        child = PsychologicalKnowledgeChild(
            id=child_data['id'],
            content=child_data['content'],
            childrens=grandchildrens
        )
        childrens.append(child)
    
    return childrens


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='导入心理知识数据到MongoDB')
    parser.add_argument('json_file', help='JSON数据文件路径')
    args = parser.parse_args()
    
    import_psychological_data(args.json_file)


if __name__ == "__main__":
    main()
