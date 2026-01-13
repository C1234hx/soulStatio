#!/usr/bin/env python3
"""
心理知识数据导入脚本 - 直接使用pymongo
用于将JSON格式的心理知识数据直接导入到MongoDB数据库中
"""

import os
import sys
import json
import argparse
from pymongo import MongoClient


def import_psychological_data(json_file_path):
    """
    直接使用pymongo导入心理知识数据到MongoDB
    
    Args:
        json_file_path: JSON数据文件的路径
    """
    try:
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"成功读取JSON文件: {json_file_path}")
        print(f"数据总量: {len(data)}")
        
        # 连接到MongoDB
        client = MongoClient(
            host='localhost',
            port=27017,
            username='root',
            password='zxcy3025',
            authSource='admin',
            serverSelectionTimeoutMS=5000
        )
        
        # 选择数据库和集合
        db = client['soulstation_db']
        collection = db['psychological_knowledge']
        
        # 清除现有数据
        collection.delete_many({})
        print("已清除现有数据")
        
        # 插入数据
        result = collection.insert_many(data)
        
        print(f"\n✅ 数据导入完成!")
        print(f"共导入 {len(result.inserted_ids)} 条心理知识数据")
        print(f"插入的ID列表: {result.inserted_ids}")
        
        # 关闭连接
        client.close()
        
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 {json_file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ 错误: 无法解析JSON文件 {json_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: 导入失败 - {str(e)}")
        sys.exit(1)


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='导入心理知识数据到MongoDB')
    parser.add_argument('json_file', help='JSON数据文件路径')
    args = parser.parse_args()
    
    import_psychological_data(args.json_file)


if __name__ == "__main__":
    main()
