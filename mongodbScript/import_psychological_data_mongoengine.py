#!/usr/bin/env python3
"""
使用MongoEngine导入心理知识数据
"""

import os
import sys
import json
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soulStation.settings")
django.setup()

from api.models import PsychologicalKnowledge

def import_psychological_data(json_file_path):
    """
    使用MongoEngine导入心理知识数据
    
    Args:
        json_file_path: JSON数据文件的路径
    """
    try:
        # 读取JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"成功读取JSON文件: {json_file_path}")
        print(f"数据总量: {len(data)}")
        
        # 暂时注释掉删除现有数据的步骤，直接插入新数据
        # PsychologicalKnowledge.objects.delete()
        # print("已清除现有数据")
        
        # 插入数据
        inserted_count = 0
        for item in data:
            knowledge = PsychologicalKnowledge(**item)
            knowledge.save()
            inserted_count += 1
        
        print(f"\n✅ 数据导入完成!")
        print(f"共导入 {len(data)} 条心理知识数据")
        
        # 验证导入结果
        count = PsychologicalKnowledge.objects.count()
        print(f"数据库中现有 {count} 条记录")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 {json_file_path}")
        return False
    except json.JSONDecodeError:
        print(f"❌ 错误: 无法解析JSON文件 {json_file_path}")
        return False
    except Exception as e:
        print(f"❌ 错误: 导入失败 - {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python import_psychological_data_mongoengine.py <json_file_path>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    import_psychological_data(json_file_path)
