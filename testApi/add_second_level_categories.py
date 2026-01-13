#!/usr/bin/env python
"""
为知识图谱详情表的每个子分类添加第二层子分类
"""

import os
import sys
import random

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soulStation.settings")
import django
django.setup()

from api.models import PsychologicalKnowledgeDetail

def add_second_level_categories():
    """为每个现有的子分类添加一个新的子分类"""
    print("\n=== 为知识图谱详情表的每个子分类添加第二层子分类 ===")
    
    # 获取所有现有的第一层子分类
    existing_categories = PsychologicalKnowledgeDetail.objects.all()
    print(f"找到 {existing_categories.count()} 个现有的子分类")
    
    # 定义第二层子分类的标题和内容模板
    second_level_titles = [
        "基础概念", "实用技巧", "案例分析", "常见问题",
        "进阶内容", "实践方法", "注意事项", "延伸阅读"
    ]
    
    content_templates = [
        "这是{parent_title}下的{title}，详细介绍相关内容",
        "{title}是{parent_title}的重要组成部分，帮助深入理解",
        "{title}提供了{parent_title}的实用工具和方法"
    ]
    
    added_count = 0
    
    for parent_category in existing_categories:
        try:
            # 随机选择一个标题和内容模板
            title = second_level_titles[added_count % len(second_level_titles)]
            content_template = random.choice(content_templates)
            content = content_template.format(parent_title=parent_category.title, title=title)
            
            # 创建新的第二层子分类
            new_category = PsychologicalKnowledgeDetail.objects.create(
                title=title,
                content=content,
                parent_id=str(parent_category.id),  # 父ID指向现有子分类的ID，转换为字符串
                parent_title=parent_category.title,  # 父标题指向现有子分类的标题
                is_active=True
            )
            
            added_count += 1
            print(f"已为 {parent_category.title} 添加子分类: {title}")
            print(f"  - 父ID: {parent_category.id}")
            print(f"  - 父标题: {parent_category.title}")
            print(f"  - 新子分类ID: {new_category.id}")
            
        except Exception as e:
            print(f"添加子分类失败: {parent_category.title}，错误: {str(e)}")
    
    print(f"\n添加完成，共添加 {added_count} 个第二层子分类")
    
    # 验证结果
    total_categories = PsychologicalKnowledgeDetail.objects.count()
    print(f"现在知识图谱详情表共有 {total_categories} 个子分类")

def verify_structure():
    """验证添加后的层级结构"""
    print("\n=== 验证层级结构 ===")
    
    # 获取所有分类
    all_categories = PsychologicalKnowledgeDetail.objects.all()
    
    # 按父ID分组
    parent_groups = {}
    for category in all_categories:
        if category.parent_id not in parent_groups:
            parent_groups[category.parent_id] = []
        parent_groups[category.parent_id].append(category)
    
    print(f"共有 {len(parent_groups)} 个不同的父ID")
    
    # 查看前几个父ID组的内容
    print("\n查看部分层级结构:")
    for i, (parent_id, categories) in enumerate(list(parent_groups.items())[:3]):
        print(f"\n父ID {parent_id} 下的分类:")
        for category in categories:
            print(f"  - {category.title} (父标题: {category.parent_title})")

if __name__ == "__main__":
    print("开始为知识图谱详情表的每个子分类添加第二层子分类...")
    add_second_level_categories()
    verify_structure()
    print("\n操作完成！")
