from mongoengine import Document, StringField, IntField, DateTimeField, BooleanField, EmbeddedDocument, EmbeddedDocumentField, ListField, ReferenceField
from bson import ObjectId
from datetime import datetime

# 用户模型
class User(Document):
    username = StringField(unique=True, max_length=50)  # 账号
    name = StringField(max_length=50)  # 名称
    password = StringField(max_length=100)  # 密码
    age = IntField(min_value=0, max_value=150)
    is_admin = BooleanField(default=False)  # 是否管理员
    is_active = BooleanField(default=True)  # 启用状态
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    # 微信登录相关字段
    openid = StringField(unique=True, max_length=100)  # 微信openid
    nickname = StringField(max_length=50)  # 微信昵称
    avatar = StringField(max_length=255)  # 微信头像
    
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

# 心理知识模型（仅存储主分类）
class PsychologicalKnowledge(Document):
    title = StringField(required=True, max_length=20)  # 标题
    content = StringField(required=True, max_length=500)  # 内容
    is_active = BooleanField(default=True)  # 启用状态
    
    meta = {
        'collection': 'psychological_knowledge'
    }

# 心理知识详情模型（存储子分类）
class PsychologicalKnowledgeDetail(Document):
    title = StringField(required=True, max_length=20)  # 标题
    content = StringField(required=True, max_length=500)  # 内容
    parent_id = StringField(required=True, max_length=24)  # 父节点ID，指向大分类的id
    parent_title = StringField(max_length=20, default=None)  # 父分类标题，最顶层节点为None
    is_active = BooleanField(default=True)  # 启用状态
    meta = {
        'collection': 'psychological_knowledge_detail'
    }

# 心理知识问答模型（用于存放心理知识问答数据）
class PsychologicalQnA(Document):
    question = StringField(required=True, max_length=200)  # 问题
    answer = StringField(required=True, max_length=1000)  # 答案
    category = StringField(required=True, max_length=50)  # 分类
    is_active = BooleanField(default=True)  # 启用状态
    created_at = DateTimeField(default=datetime.now)  # 创建时间
    
    meta = {
        'collection': 'psychological_qna',
        'ordering': ['-created_at']
    }
