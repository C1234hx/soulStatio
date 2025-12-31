from mongoengine import Document, StringField, IntField, DateTimeField, BooleanField
from datetime import datetime

# 用户模型
class User(Document):
    username = StringField(required=True, unique=True, max_length=50)  # 账号
    name = StringField(required=True, max_length=50)  # 名称
    password = StringField(required=True, max_length=100)  # 密码
    age = IntField(min_value=0, max_value=150)
    is_admin = BooleanField(default=False)  # 是否管理员
    is_active = BooleanField(default=True)  # 启用状态
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'users',
        'ordering': ['-created_at']
    }

# 行动建议模型
class ActionAdvice(Document):
    emotion_direction = IntField(required=True, min_value=1, max_value=3)  # 情绪向：1-正向，2-普通，3-负向（0用于筛选全部）
    content = StringField(required=True, max_length=70)  # 行动建议内容，最大长度70个字符
    is_active = BooleanField(default=True)  # 启用状态
    created_at = DateTimeField(default=datetime.now)  # 创建时间
    
    meta = {
        'collection': 'action_advice',
        'ordering': ['-created_at']
    }
