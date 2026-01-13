#!/usr/bin/env python
"""
心理知识数据清理与更新脚本
1. 清理psychological_knowledge集合中的category和父节点字段
2. 为psychological_knowledge_detail集合中的子分类添加父节点标题
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soulStation.settings")
import django
django.setup()

from api.models import PsychologicalKnowledge, PsychologicalKnowledgeDetail
from mongoengine.connection import get_db

def cleanup_psychological_knowledge():
    """清理psychological_knowledge集合中的category和父节点字段"""
    print("\n=== 清理psychological_knowledge集合 ===")
    
    # 获取数据库连接
    db = get_db()
    collection = db.psychological_knowledge
    
    # 检查并移除category字段
    try:
        result = collection.update_many({}, {"$unset": {"category": ""}})
        print(f"已移除category字段，影响记录数: {result.modified_count}")
    except Exception as e:
        print(f"移除category字段失败: {str(e)}")
    
    # 检查并移除parent_title字段
    try:
        result = collection.update_many({}, {"$unset": {"parent_title": ""}})
        print(f"已移除parent_title字段，影响记录数: {result.modified_count}")
    except Exception as e:
        print(f"移除parent_title字段失败: {str(e)}")
    
    # 检查并移除parent_id字段（如果存在）
    try:
        result = collection.update_many({}, {"$unset": {"parent_id": ""}})
        print(f"已移除parent_id字段，影响记录数: {result.modified_count}")
    except Exception as e:
        print(f"移除parent_id字段失败: {str(e)}")

def update_psychological_knowledge_detail():
    """为psychological_knowledge_detail集合中的子分类添加父节点标题"""
    print("\n=== 更新psychological_knowledge_detail集合 ===")
    
    # 获取所有主分类数据
    main_categories = PsychologicalKnowledge.objects.all()
    print(f"找到 {main_categories.count()} 个主分类")
    
    # 创建主分类ID到标题的映射
    main_category_map = {}
    for category in main_categories:
        main_category_map[str(category.id)] = category.title
        print(f"主分类: {str(category.id)} -> {category.title}")
    
    # 更新每个子分类的parent_title字段
    updated_count = 0
    total_count = 0
    
    for detail in PsychologicalKnowledgeDetail.objects.all():
        total_count += 1
        parent_id = detail.parent_id
        
        if parent_id in main_category_map:
            # 获取对应的主分类标题
            parent_title = main_category_map[parent_id]
            
            if detail.parent_title != parent_title:
                # 更新parent_title字段
                detail.parent_title = parent_title
                detail.save()
                updated_count += 1
                print(f"更新子分类: {detail.title} -> 父标题: {parent_title}")
            else:
                print(f"子分类: {detail.title} 的父标题已正确设置")
        else:
            print(f"警告: 子分类 {detail.title} 的父分类ID {parent_id} 未找到对应的主分类")
    
    print(f"\n更新完成: 共检查 {total_count} 个子分类，更新 {updated_count} 个")

def verify_data():
    """验证数据更新结果"""
    print("\n=== 验证数据更新结果 ===")
    
    # 验证psychological_knowledge集合
    print("\n1. 验证psychological_knowledge集合:")
    main_categories = PsychologicalKnowledge.objects.all()
    print(f"主分类总数: {main_categories.count()}")
    
    if main_categories.count() > 0:
        # 检查第一个主分类的字段
        first_category = main_categories.first()
        print(f"第一个主分类字段: {first_category._data.keys()}")
        print(f"主分类: {first_category.title} - 内容: {first_category.content}")
    
    # 验证psychological_knowledge_detail集合
    print("\n2. 验证psychological_knowledge_detail集合:")
    details = PsychologicalKnowledgeDetail.objects.all()
    print(f"子分类总数: {details.count()}")
    
    if details.count() > 0:
        # 检查前5个子分类的字段
        for i, detail in enumerate(details[:5]):
            print(f"子分类 {i+1}: {detail.title} - 父ID: {detail.parent_id} - 父标题: {detail.parent_title}")

if __name__ == "__main__":
    print("开始执行心理知识数据清理与更新...")
    
    # 执行清理操作
    cleanup_psychological_knowledge()
    
    # 执行更新操作
    update_psychological_knowledge_detail()
    
    # 验证结果
    verify_data()
    
    print("\n数据清理与更新完成！")
