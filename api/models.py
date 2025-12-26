from mongoengine import Document, StringField, IntField, DateTimeField, BooleanField
from datetime import datetime

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
