#!/usr/bin/env python
"""
测试数据生成脚本
为每个情绪向(0-3)添加2条符合内容长度限制的行动建议
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soulStation.settings")
import django
django.setup()

from api.models import ActionAdvice

def generate_test_data():
    """生成测试数据"""
    # 定义测试数据，每个情绪向2条内容，每条内容不超过70个字符
    test_data = [
        # 情绪向1-正向
        {'emotion_direction': 1, 'content': '今天的阳光真温暖，心情也变得格外愉悦'},  # 23个字符
        {'emotion_direction': 1, 'content': '努力总会有收获，坚持就是胜利'},  # 18个字符
        
        # 情绪向2-普通
        {'emotion_direction': 2, 'content': '生活需要慢慢品味，珍惜每一个瞬间'},  # 22个字符
        {'emotion_direction': 2, 'content': '保持平衡的生活节奏，让自己更加充实'},  # 24个字符
        
        # 情绪向3-负向
        {'emotion_direction': 3, 'content': '学会释放内心的压力，给自己一点空间'},  # 24个字符
        {'emotion_direction': 3, 'content': '困难只是暂时的挑战，相信自己能克服'},  # 24个字符
    ]
    
    # 批量创建测试数据
    created_count = 0
    for data in test_data:
        try:
            # 验证内容长度
            if len(data['content']) > 70:
                print(f"警告：内容 '{data['content']}' 超过70个字符，将被截断")
                data['content'] = data['content'][:70]
            
            ActionAdvice.objects.create(**data)
            created_count += 1
            print(f"成功创建：情绪向{data['emotion_direction']} - {data['content']}")
        except Exception as e:
            print(f"创建失败：{data}，错误：{str(e)}")
    
    print(f"\n测试数据生成完成，共创建 {created_count} 条记录")
    
    # 验证数据
    print("\n验证数据：")
    for emotion_direction in range(1, 4):  # 只验证情绪向1-3
        count = ActionAdvice.objects.filter(emotion_direction=emotion_direction).count()
        print(f"情绪向 {emotion_direction}：{count} 条记录")
    
    # 统计总记录数
    total_count = ActionAdvice.objects.count()
    print(f"\n总记录数：{total_count} 条")

if __name__ == "__main__":
    print("开始生成行动建议测试数据...")
    generate_test_data()