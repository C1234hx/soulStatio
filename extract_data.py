#!/usr/bin/env python
"""
提取符合条件的JSON数据
将第一级分类为"一、"，第二级别为"1."格式的论文数据提取出来
"""

import json
import re
import os

def extract_qualified_papers():
    """
    提取符合条件的论文数据
    """
    # 文件路径
    input_file = r"C:/Users/EDY/Desktop/soulStation/crawler/psychological_papers_detail.json"
    output_file = r"C:/Users/EDY/Desktop/soulStation/crawler/extracted_papers.json"
    
    try:
        # 读取原文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("JSON文件内容不是列表格式")
            return
        
        print(f"原文件共有 {len(data)} 条记录")
        
        # 提取符合条件的数据
        qualified_papers = []
        
        # 定义正则表达式模式
        first_level_pattern = re.compile(r'(?:一|二|三|四|五|六|七|八|九|十)+、')  # 第一级标题：一、
        second_level_pattern = re.compile(r'\d+\.\s*')  # 第二级标题：1. 2. 等
        
        for i, paper in enumerate(data):
            if isinstance(paper, dict):
                content = paper.get("content", "")
                
                # 检查是否同时包含第一级和第二级标题
                if first_level_pattern.search(content) and second_level_pattern.search(content):
                    qualified_papers.append(paper)
                    print(f"找到符合条件的论文: {paper.get('title', f'无标题-{i}')}")
        
        print(f"\n共找到 {len(qualified_papers)} 条符合条件的论文")
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(qualified_papers, f, ensure_ascii=False, indent=2)
        
        print(f"结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    extract_qualified_papers()