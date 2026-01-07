#!/usr/bin/env python
"""创建初始心理咨询聊天数据"""

import os
import sys

# 添加Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soulStation.settings')

import django
django.setup()

from api.models import PsychologicalChat

# 初始对话数据（5组user提问和ai回答）
initial_chats = [
    # 第1组对话
    {"sender": "user", "content": "最近工作压力很大，总是感到焦虑不安，我该怎么办？"},
    {"sender": "ai", "content": "工作压力大感到焦虑是很常见的情绪反应。建议你尝试分解任务，设定合理的工作目标，每天预留一些时间进行放松活动，比如深呼吸、散步或者听音乐。也可以考虑和同事或朋友聊聊你的感受，寻求支持和理解。"},
    
    # 第2组对话
    {"sender": "user", "content": "我和家人的关系越来越紧张，经常因为小事争吵，不知道如何改善。"},
    {"sender": "ai", "content": "家人之间的争吵往往源于沟通方式的问题。建议你在沟通时尝试使用'我'语句表达感受，而不是指责对方。比如'我感到难过'而不是'你总是惹我生气'。同时，也要学会倾听家人的想法和感受，给予彼此更多的理解和包容。"},
    
    # 第3组对话
    {"sender": "user", "content": "我总是担心自己做不好事情，害怕失败，这种心理影响了我的工作和生活。"},
    {"sender": "ai", "content": "对失败的恐惧是很多人都会有的心理。首先要认识到失败是成长的一部分，每个人都会经历。尝试设定小目标，逐步积累成功经验，增强自信心。同时，也要学会接受自己的不完美，给自己一些宽容和鼓励。"},
    
    # 第4组对话
    {"sender": "user", "content": "最近睡眠质量很差，经常失眠，白天精神状态也不好。"},
    {"sender": "ai", "content": "失眠可能与压力、生活习惯等因素有关。建议你保持规律的作息时间，睡前避免使用电子设备，创造一个舒适的睡眠环境。可以尝试一些放松技巧，比如冥想、温水泡脚或阅读轻松的书籍。如果问题持续存在，建议咨询医生的意见。"},
    
    # 第5组对话
    {"sender": "user", "content": "我觉得自己很孤独，身边没有真正理解我的朋友。"},
    {"sender": "ai", "content": "孤独感是一种常见的情绪体验。尝试主动参与一些自己感兴趣的活动，扩大社交圈子，结识志同道合的朋友。同时，也要学会与自己相处，培养一些独处时的兴趣爱好。记住，真正的友谊需要时间和精力去维护，不要急于求成。"},
]

def create_initial_chats():
    """创建初始聊天数据"""
    try:
        # 清空现有数据（可选）
        # PsychologicalChat.objects.all().delete()
        
        # 添加初始数据
        for chat in initial_chats:
            PsychologicalChat.objects.create(**chat)
        
        print(f"成功创建{len(initial_chats)}条初始聊天数据！")
        print("\n创建的数据：")
        for chat in PsychologicalChat.objects.all().order_by('created_at'):
            print(f"[{chat.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {chat.sender}: {chat.content}")
            
    except Exception as e:
        print(f"创建初始数据失败：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_initial_chats()
