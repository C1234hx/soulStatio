#!/usr/bin/env python
"""
心理知识测试数据生成脚本
为心理知识数据表生成适合ECharts关系图的测试数据
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

from api.models import PsychologicalKnowledge, PsychologicalKnowledgeDetail

def generate_psychological_knowledge_data():
    """生成心理知识测试数据"""
    
    # 清空现有数据
    PsychologicalKnowledge.objects.delete()
    PsychologicalKnowledgeDetail.objects.delete()
    print("已清空现有心理知识数据")
    
    # 定义主分类数据
    main_categories = [
        {"title": "情绪管理", "content": "学习如何识别和调节情绪的基本概念"},
        {"title": "认知行为", "content": "探索思维、情绪和行为之间的关系"},
        {"title": "人际关系", "content": "建立和维护健康人际关系的技巧"},
        {"title": "压力应对", "content": "有效管理和减轻压力的方法"},
        {"title": "自我成长", "content": "促进个人发展和自我实现的途径"}
    ]
    
    # 定义子分类数据模板
    subcategory_templates = [
        {"content": "这是{parent_title}下的子分类内容，详细介绍相关概念和技巧"},
        {"content": "{parent_title}的重要组成部分，帮助深入理解主题"},
        {"content": "实用的{parent_title}工具和方法，可直接应用于日常生活"}
    ]
    
    main_created_count = 0
    detail_created_count = 0
    main_category_map = {}
    
    # 创建主分类
    print("\n创建主分类：")
    for category in main_categories:
        try:
            main_node = PsychologicalKnowledge.objects.create(
                title=category["title"],
                content=category["content"],
                is_active=True
            )
            main_category_map[str(main_node.id)] = {
                "title": category["title"],
                "node": main_node
            }
            main_created_count += 1
            print(f"成功创建主分类：{category['title']}")
        except Exception as e:
            print(f"创建主分类失败：{category['title']}，错误：{str(e)}")
    
    # 创建子分类
    print("\n创建子分类：")
    subcategory_titles = [
        "识别情绪", "表达情绪", "调节情绪", "情绪健康",
        "认知模式", "思维误区", "行为改变", "认知重构",
        "沟通技巧", "边界设置", "冲突解决", "同理心培养",
        "压力识别", "放松技巧", "时间管理", "优先级设置",
        "目标设定", "自我接纳", "技能培养", "成长心态"
    ]
    
    # 为每个主分类创建子分类
    for main_id, main_info in main_category_map.items():
        # 为每个主分类分配4个子分类
        for i in range(4):
            try:
                title = subcategory_titles.pop(0) if subcategory_titles else f"子分类{detail_created_count + 1}"
                template = random.choice(subcategory_templates)
                content = template["content"].format(parent_title=main_info["title"])
                
                PsychologicalKnowledgeDetail.objects.create(
                    title=title,
                    content=content,
                    parent_id=main_id,  # 关联主分类ID
                    parent_title=None,  # 最顶层子节点的父分类标题为None
                    is_active=True
                )
                detail_created_count += 1
                print(f"成功创建子分类：{title} (父分类：{main_info['title']})")
            except Exception as e:
                print(f"创建子分类失败：{title}，错误：{str(e)}")
    
    print(f"\n测试数据生成完成：")
    print(f"主分类：{main_created_count} 条记录")
    print(f"子分类：{detail_created_count} 条记录")
    print(f"总记录数：{main_created_count + detail_created_count} 条")
    
    # 验证数据
    print("\n验证数据：")
    main_count = PsychologicalKnowledge.objects.count()
    detail_count = PsychologicalKnowledgeDetail.objects.count()
    print(f"主分类表记录数：{main_count}")
    print(f"详情表记录数：{detail_count}")
    
    # 验证详情表中的parent_id和parent_title
    first_detail = PsychologicalKnowledgeDetail.objects.first()
    if first_detail:
        print(f"\n详情表第一条记录：")
        print(f"  ID: {first_detail.id}")
        print(f"  标题: {first_detail.title}")
        print(f"  内容: {first_detail.content}")
        print(f"  父节点ID: {first_detail.parent_id}")
        print(f"  父分类标题: {first_detail.parent_title}")
        print(f"  启用状态: {first_detail.is_active}")

if __name__ == "__main__":
    print("开始生成心理知识测试数据...")
    generate_psychological_knowledge_data()
