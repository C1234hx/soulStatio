#!/usr/bin/env python
"""
测试心理知识主分类的关键词搜索功能
"""

import requests
import json

base_url = "http://127.0.0.1:8000/api"

def test_search_without_keyword():
    """测试不带关键词的查询（应该返回全部数据）"""
    print("\n=== 测试不带关键词的查询 ===")
    
    url = f"{base_url}/psychological-knowledge/main/"
    response = requests.get(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("响应数据:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        
        if data.get("code") == 200:
            categories = data.get("data", [])
            print(f"\n获取到 {len(categories)} 个主分类")
            return categories
        else:
            print("\n接口返回错误码:", data.get("code"))
            return []
            
    else:
        print(f"\n请求失败，状态码: {response.status_code}")
        print("响应内容:", response.text)
        return []

def test_search_by_title():
    """测试通过标题搜索"""
    print("\n=== 测试通过标题搜索（关键词: '情绪'） ===")
    
    url = f"{base_url}/psychological-knowledge/main/?keyword=情绪"
    response = requests.get(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("响应数据:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        
        if data.get("code") == 200:
            categories = data.get("data", [])
            print(f"\n获取到 {len(categories)} 个主分类")
            return categories
        else:
            print("\n接口返回错误码:", data.get("code"))
            return []
            
    else:
        print(f"\n请求失败，状态码: {response.status_code}")
        print("响应内容:", response.text)
        return []

def test_search_by_content():
    """测试通过内容搜索"""
    print("\n=== 测试通过内容搜索（关键词: '压力'） ===")
    
    url = f"{base_url}/psychological-knowledge/main/?keyword=压力"
    response = requests.get(url)
    
    print(f"请求URL: {url}")
    print(f"响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("响应数据:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        
        if data.get("code") == 200:
            categories = data.get("data", [])
            print(f"\n获取到 {len(categories)} 个主分类")
            return categories
        else:
            print("\n接口返回错误码:", data.get("code"))
            return []
            
    else:
        print(f"\n请求失败，状态码: {response.status_code}")
        print("响应内容:", response.text)
        return []

if __name__ == "__main__":
    print("开始测试心理知识主分类的关键词搜索功能...")
    
    # 测试不带关键词的查询
    all_categories = test_search_without_keyword()
    
    # 测试通过标题搜索
    title_search_categories = test_search_by_title()
    
    # 测试通过内容搜索
    content_search_categories = test_search_by_content()
    
    print("\n=== 测试总结 ===")
    print(f"不带关键词查询: {len(all_categories)} 个结果")
    print(f"标题搜索 (关键词: '情绪'): {len(title_search_categories)} 个结果")
    print(f"内容搜索 (关键词: '压力'): {len(content_search_categories)} 个结果")
    print("\n所有测试完成！")
