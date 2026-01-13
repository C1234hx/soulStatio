#!/usr/bin/env python
"""
心理知识API测试脚本
测试心理知识主分类和详情接口是否正常工作
"""

import requests
import json

base_url = "http://127.0.0.1:8000/api"

def test_psychological_knowledge_main_list():
    """测试获取所有主分类数据接口"""
    print("\n=== 测试获取心理知识主分类列表接口 ===")
    
    url = f"{base_url}/psychological-knowledge/main/"
    response = requests.get(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("响应数据:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
            
            if data.get("code") == 200:
                main_categories = data.get("data", [])
                print(f"\n获取到 {len(main_categories)} 个主分类")
                return main_categories
            else:
                print("\n接口返回错误码:", data.get("code"))
                return []
                
        except json.JSONDecodeError:
            print("\n响应数据不是有效的JSON格式")
            return []
    else:
        print(f"\n请求失败，状态码: {response.status_code}")
        print("响应内容:", response.text)
        return []

def test_psychological_knowledge_detail_by_parent_id(parent_id):
    """测试根据主分类id查询子分类数据接口"""
    print(f"\n=== 测试获取心理知识详情接口 (parent_id: {parent_id}) ===")
    
    url = f"{base_url}/psychological-knowledge/detail/{parent_id}/"
    response = requests.get(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("响应数据:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
            
            if data.get("code") == 200:
                details = data.get("data", [])
                print(f"\n获取到 {len(details)} 个子分类")
                return details
            else:
                print("\n接口返回错误码:", data.get("code"))
                return []
                
        except json.JSONDecodeError:
            print("\n响应数据不是有效的JSON格式")
            return []
    else:
        print(f"\n请求失败，状态码: {response.status_code}")
        print("响应内容:", response.text)
        return []

if __name__ == "__main__":
    print("开始测试心理知识API接口...")
    
    # 测试主分类接口
    main_categories = test_psychological_knowledge_main_list()
    
    # 测试详情接口
    if main_categories:
        # 测试第一个主分类的详情接口
        first_main_id = main_categories[0]["id"]
        test_psychological_knowledge_detail_by_parent_id(first_main_id)
        
        # 测试最后一个主分类的详情接口
        last_main_id = main_categories[-1]["id"]
        test_psychological_knowledge_detail_by_parent_id(last_main_id)
    
    print("\n所有API测试完成！")
