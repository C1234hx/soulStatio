#!/usr/bin/env python
"""
测试行动建议API的筛选和搜索功能
"""

import requests

base_url = 'http://127.0.0.1:8000/api/action-advice/'

def test_api_functionality():
    print("测试行动建议API的筛选和搜索功能...")
    print("="*50)
    
    # 测试1: 获取所有行动建议
    print("1. 测试获取所有行动建议:")
    response = requests.get(base_url)
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回记录数: {len(data)}")
    print()
    
    # 测试2: 按情绪向筛选 - 正向(1)
    print("2. 测试按情绪向筛选 - 正向(1):")
    params = {'emotion_direction': 1}
    response = requests.get(base_url, params=params)
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回记录数: {len(data)}")
    # 验证返回的记录情绪向是否正确
    if data:
        print(f"第一条记录情绪向: {data[0]['emotion_direction']}")
    print()
    
    # 测试3: 按情绪向筛选 - 普通(2)
    print("3. 测试按情绪向筛选 - 普通(2):")
    params = {'emotion_direction': 2}
    response = requests.get(base_url, params=params)
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回记录数: {len(data)}")
    if data:
        print(f"第一条记录情绪向: {data[0]['emotion_direction']}")
    print()
    
    # 测试4: 按情绪向筛选 - 负向(3)
    print("4. 测试按情绪向筛选 - 负向(3):")
    params = {'emotion_direction': 3}
    response = requests.get(base_url, params=params)
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回记录数: {len(data)}")
    if data:
        print(f"第一条记录情绪向: {data[0]['emotion_direction']}")
    print()
    
    # 测试5: 按情绪向筛选 - 全部(0)
    print("5. 测试按情绪向筛选 - 全部(0):")
    params = {'emotion_direction': 0}
    response = requests.get(base_url, params=params)
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回记录数: {len(data)}")
    print()
    
    # 测试6: 内容模糊搜索 - 包含"阳光"
    print("6. 测试内容模糊搜索 - 包含'阳光':")
    params = {'content': '阳光'}
    response = requests.get(base_url, params=params)
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回记录数: {len(data)}")
    if data:
        print(f"匹配的内容: {[item['content'] for item in data]}")
    print()
    
    # 测试7: 内容模糊搜索 - 包含"压力"
    print("7. 测试内容模糊搜索 - 包含'压力':")
    params = {'content': '压力'}
    response = requests.get(base_url, params=params)
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回记录数: {len(data)}")
    if data:
        print(f"匹配的内容: {[item['content'] for item in data]}")
    print()
    
    # 测试8: 组合筛选 - 正向(1)且包含"努力"
    print("8. 测试组合筛选 - 正向(1)且包含'努力':")
    params = {'emotion_direction': 1, 'content': '努力'}
    response = requests.get(base_url, params=params)
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"返回记录数: {len(data)}")
    if data:
        print(f"匹配的记录: {data}")
    print()
    
    print("="*50)
    print("测试完成!")

if __name__ == "__main__":
    test_api_functionality()