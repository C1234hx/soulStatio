#!/usr/bin/env python
"""
基础简约的爬虫脚本示例
使用requests获取网页内容，BeautifulSoup解析HTML
"""

import requests
import json
import os
from bs4 import BeautifulSoup


def simple_crawler():
    list = []
    for i in range(1,77):
        # 目标网站URL（选择一个简单的、允许爬取的网站）
        if i==1:
            url = "https://www.lunwendata.com/thesis/List_115.html"
        else:
            url = f"https://www.lunwendata.com/thesis/List_115_{i}.html"
        
        print(f"开始爬取网站: {url}")
        try:
            # 发送HTTP请求获取网页内容，设置超时和编码
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            
            # 尝试自动识别网页编码
            response.encoding = response.apparent_encoding
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取网页标题
            page_title = soup.title.string
            print(f"\n网页标题: {page_title}")
            
            # 提取文章标题和链接（根据实际HTML结构调整选择器）
            print("\n最新文章列表:")
            
            # 查找所有文章元素（这里需要根据目标网站的HTML结构调整选择器）
            articles = soup.find_all('li')
            
            
            for article in articles:
                # 提取标题
                title = article.find('a')
                # 提取链接
                link = title['href'] if title and 'href' in title.attrs else "无链接"
                
                list.append({
                    'title': title.text.strip() if title else "无标题",
                    'link': link
                })
                
            print(f"\n爬取完成，共获取 {len(articles)} 篇文章")
            print(list)
            
        except requests.RequestException as e:
            print(f"请求失败: {str(e)}")
        except Exception as e:
            print(f"解析失败: {str(e)}")
        
    # 将数据保存为JSON文件
    save_to_json(list, "psychological_papers.json")
    


def save_to_json(data, filename):
    """将数据保存为JSON文件"""
    try:
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, filename)
        
        # 写入JSON文件，确保中文正常显示
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n数据已成功保存到: {file_path}")
    except Exception as e:
        print(f"保存JSON文件失败: {str(e)}")


def save_detail():
    """保存文章详情"""
    # 读取JSON文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'psychological_papers.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 遍历每篇文章，获取详情
    for item in data:
        title = item['title']
        link = item['link']
        
        print(f"正在获取文章详情: {title} ({link})")
        
        try:
            # 发送HTTP请求获取文章详情
            response = requests.get(link, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取文章内容（根据实际HTML结构调整选择器）
            content = soup.find('div', id='content')
            if content:
                item['content'] = content.get_text(separator='\n', strip=True)
                print(item['content'],'---------------------------------------内容-------------------------------------')
            else:
                item['content'] = "无内容"
            
            print(f"成功获取文章详情: {title}")
        
        except requests.RequestException as e:
            print(f"请求失败: {str(e)}")
        except Exception as e:
            print(f"解析失败: {str(e)}")
    save_to_json(data, "psychological_papers_detail.json")

if __name__ == "__main__":
    save_detail()
