#!/usr/bin/env python
"""
提取符合精确条件的JSON数据
只提取包含"一、"格式一级标题和"1."格式二级标题，且不包含其他格式标题的论文数据
"""

import json
import re
import os

def extract_exact_papers():
    """
    提取符合精确条件的论文数据
    """
    # 文件路径
    input_file = r"C:/Users/EDY/Desktop/soulStation/crawler/psychological_papers_detail.json"
    output_file = r"C:/Users/EDY/Desktop/soulStation/crawler/exact_papers.json"
    
    try:
        # 读取原文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("JSON文件内容不是列表格式")
            return
        
        print(f"原文件共有 {len(data)} 条记录")
        
        # 定义正则表达式模式
        first_level_pattern = re.compile(r'(?:一|二|三|四|五|六|七|八|九|十)+、')  # 第一级标题：一、
        second_level_pattern = re.compile(r'\d+\.\s*')  # 第二级标题：1. 2. 等
        other_level_patterns = [
            re.compile(r'\(\d+\)'),  # 排除：(1) (2) 等
            re.compile(r'\d+\.\d+'),  # 排除：1.1 1.2 等
            re.compile(r'[\u4e00-\u9fa5]+\d+'),  # 排除：第一 第二 等
            re.compile(r'[a-zA-Z]+\.'),  # 排除：a. b. 等
            re.compile(r'\d+\s*[、]')  # 排除：1、 2、 等
        ]
        
        # 提取符合条件的数据
        exact_papers = []
        
        for i, paper in enumerate(data):
            if isinstance(paper, dict):
                content = paper.get("content", "")
                
                # 必须同时包含第一级和第二级标题
                has_first_level = bool(first_level_pattern.search(content))
                has_second_level = bool(second_level_pattern.search(content))
                
                # 必须不包含其他格式的标题
                has_other_level = False
                for pattern in other_level_patterns:
                    if pattern.search(content):
                        has_other_level = True
                        break
                
                if has_first_level and has_second_level and not has_other_level:
                    exact_papers.append(paper)
                    print(f"找到符合条件的论文: {paper.get('title', f'无标题-{i}')}")
        
        print(f"\n共找到 {len(exact_papers)} 条符合精确条件的论文")
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(exact_papers, f, ensure_ascii=False, indent=2)
        
        print(f"结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    extract_exact_papers()