from mongoengine import Document, StringField, IntField, DateTimeField, BooleanField, EmbeddedDocument, EmbeddedDocumentField, ListField, ReferenceField
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

# 鸡汤数据模型
class ChickenSoup(Document):
    content = StringField(required=True, max_length=70)  # 鸡汤内容，最大长度70个字符
    is_active = BooleanField(default=True)  # 启用状态
    created_at = DateTimeField(default=datetime.now)  # 创建时间
    
    meta = {
        'collection': 'chicken_soup',
        'ordering': ['-created_at']
    }

# 心理咨询聊天数据模型
class PsychologicalChat(Document):
    sender = StringField(required=True, choices=['user', 'ai'])  # 发送人：user或ai
    content = StringField(required=True, max_length=1000)  # 发送内容，最大1000字符
    created_at = DateTimeField(default=datetime.now)  # 创建时间
    
    meta = {
        'collection': 'psychological_chat',
        'ordering': ['-created_at']
    }

# 心理知识子分类嵌入式文档
class PsychologicalKnowledgeChild(EmbeddedDocument):
    id = StringField(required=True, primary_key=True)  # 子分类ID
    content = StringField(required=True, max_length=500)  # 子分类内容
    childrens = ListField(EmbeddedDocumentField('self'), default=list)  # 递归嵌套子分类
    is_active = BooleanField(default=True)  # 启用状态
    created_at = DateTimeField(default=datetime.now)  # 创建时间

# 心理知识主分类模型
class PsychologicalKnowledge(Document):
    id = StringField(required=True, primary_key=True)  # 主分类ID
    content = StringField(required=True, max_length=500)  # 主分类内容
    childrens = ListField(EmbeddedDocumentField(PsychologicalKnowledgeChild), default=list)  # 子分类列表
    is_active = BooleanField(default=True)  # 启用状态
    created_at = DateTimeField(default=datetime.now)  # 创建时间
    updated_at = DateTimeField(default=datetime.now)  # 更新时间
    
    meta = {
        'collection': 'psychological_knowledge',
        'ordering': ['-created_at']
    }
