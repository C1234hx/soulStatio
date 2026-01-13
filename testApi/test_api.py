#!/usr/bin/env python3
"""
测试心理知识API接口的脚本
"""

import requests

def test_psychological_knowledge_api():
    """
    测试心理知识API接口
    """
    try:
        # API端点URL
        url = 'http://localhost:8000/api/psychological-knowledge/'  # 注意使用连字符而不是下划线
        
        print(f"正在调用API接口: {url}")
        response = requests.get(url)
        
        print(f"\n✅ API调用成功!")
        print(f"状态码: {response.status_code}")
        
        # 解析响应数据
        data = response.json()
        print(f"响应数据: {data}")
        
        # 检查响应结构
        if response.status_code == 200 and data.get('code') == 200:
            psychological_data = data.get('data', [])
            print(f"\n✅ 心理知识数据获取成功!")
            print(f"数据总量: {len(psychological_data)}")
            
            # 打印每条数据的基本信息
            for i, item in enumerate(psychological_data, 1):
                print(f"\n数据 {i}:")
                print(f"  内容: {item.get('content')}")
                print(f"  子分类数量: {len(item.get('childrens', []))}")
                print(f"  状态: {'启用' if item.get('is_active', True) else '禁用'}")
                
                # 打印第一层子分类
                if item.get('childrens'):
                    print("  第一层子分类:")
                    for j, child in enumerate(item.get('childrens', [])[:3], 1):  # 只显示前3个子分类
                        print(f"    {j}. {child.get('content')} (子分类数量: {len(child.get('childrens', []))})")
                    if len(item.get('childrens', [])) > 3:
                        print(f"    ... 还有 {len(item.get('childrens', [])) - 3} 个子分类")
            
            return True
        else:
            print(f"❌ API调用失败: {data}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_psychological_knowledge_api()
