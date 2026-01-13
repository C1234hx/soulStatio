#!/usr/bin/env python
"""
测试知识图谱详情表的第二层子分类
"""

import requests
import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soulStation.settings")
import django
django.setup()

from api.models import PsychologicalKnowledgeDetail

base_url = "http://127.0.0.1:8000/api"

def test_second_level_categories():
    """测试第二层子分类的查询和结构"""
    print("\n=== 测试知识图谱详情表的第二层子分类 ===")
    
    # 获取所有子分类，包括第一层和第二层
    all_categories = PsychologicalKnowledgeDetail.objects.all()
    print(f"数据库中共有 {all_categories.count()} 个子分类")
    
    # 按父ID分组
    parent_groups = {}
    for category in all_categories:
        if category.parent_id not in parent_groups:
            parent_groups[category.parent_id] = []
        parent_groups[category.parent_id].append(category)
    
    print(f"共有 {len(parent_groups)} 个不同的父ID")
    
    # 找出第一层子分类（父ID是主分类ID）
    first_level_categories = []
    second_level_categories = []
    
    for parent_id, categories in parent_groups.items():
        # 检查父ID的长度，如果是主分类ID（24位），则是第一层子分类
        if len(parent_id) == 24 and categories[0].parent_title in ["情绪管理", "认知行为", "人际关系", "压力应对", "自我成长"]:
            first_level_categories.extend(categories)
        else:
            second_level_categories.extend(categories)
    
    print(f"第一层子分类数量: {len(first_level_categories)}")
    print(f"第二层子分类数量: {len(second_level_categories)}")
    
    # 验证每个第一层子分类是否有一个第二层子分类
    print("\n验证每个第一层子分类是否有一个第二层子分类:")
    for first_level in first_level_categories:
        # 查找以此分类ID为父ID的子分类
        children = PsychologicalKnowledgeDetail.objects.filter(parent_id=str(first_level.id))
        print(f"子分类: {first_level.title} (ID: {first_level.id}) - 子节点数量: {children.count()}")
        
        for child in children:
            print(f"  - 第二层子分类: {child.title} (父标题: {child.parent_title})")
    
    # 测试通过API查询第二层子分类
    print("\n=== 测试通过API查询第二层子分类 ===")
    if first_level_categories:
        # 取第一个第一层子分类的ID作为父ID查询
        first_level_id = str(first_level_categories[0].id)
        print(f"使用第一层子分类ID: {first_level_id} 查询其下的第二层子分类")
        
        url = f"{base_url}/psychological-knowledge/detail/{first_level_id}/"
        response = requests.get(url)
        
        print(f"请求URL: {url}")
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("响应数据:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
            
            if data.get("code") == 200:
                details = data.get("data", [])
                print(f"\n获取到 {len(details)} 个第二层子分类")
            else:
                print("\n接口返回错误码:", data.get("code"))
        else:
            print(f"\n请求失败，状态码: {response.status_code}")
            print("响应内容:", response.text)

if __name__ == "__main__":
    print("开始测试知识图谱详情表的第二层子分类...")
    test_second_level_categories()
    print("\n所有测试完成！")
