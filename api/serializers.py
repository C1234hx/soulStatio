from rest_framework import serializers
from .models import User, ActionAdvice, ChickenSoup, PsychologicalChat, PsychologicalKnowledge, PsychologicalKnowledgeChild

#用户序列化器
class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(required=True, max_length=50)  # 账号
    name = serializers.CharField(required=True, max_length=50)  # 名称
    password = serializers.CharField(required=True, max_length=100, write_only=True)  # 密码，仅写入
    age = serializers.IntegerField(min_value=0, max_value=150, required=False)
    is_admin = serializers.BooleanField(default=False)  # 是否管理员
    is_active = serializers.BooleanField(default=True)  # 启用状态
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.name = validated_data.get('name', instance.name)
        if 'password' in validated_data:
            instance.password = validated_data['password']
        instance.age = validated_data.get('age', instance.age)
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

# 行动建议序列化器
class ActionAdviceSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # ID，只读
    emotion_direction = serializers.IntegerField(required=True, min_value=1, max_value=3)  # 情绪向：1-正向，2-普通，3-负向
    content = serializers.CharField(required=True, max_length=70)  # 行动建议内容，最大长度70个字符
    is_active = serializers.BooleanField(default=True)  # 启用状态
    created_at = serializers.DateTimeField(read_only=True)  # 创建时间，只读
    
    def validate_content(self, value):
        """验证内容长度不超过70个字符"""
        if len(value) > 70:
            raise serializers.ValidationError("内容长度不能超过70个字符")
        return value

    def create(self, validated_data):
        """创建新的行动建议"""
        return ActionAdvice.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """更新现有行动建议"""
        instance.emotion_direction = validated_data.get('emotion_direction', instance.emotion_direction)
        instance.content = validated_data.get('content', instance.content)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

# 鸡汤数据序列化器
class ChickenSoupSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # ID，只读
    content = serializers.CharField(required=True, max_length=70)  # 鸡汤内容，最大长度70个字符
    is_active = serializers.BooleanField(default=True)  # 启用状态
    created_at = serializers.DateTimeField(read_only=True)  # 创建时间，只读
    
    def validate_content(self, value):
        """验证内容长度不超过70个字符"""
        if len(value) > 70:
            raise serializers.ValidationError("内容长度不能超过70个字符")
        return value
    
    def create(self, validated_data):
        """创建新的鸡汤数据"""
        return ChickenSoup.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """更新现有鸡汤数据"""
        instance.content = validated_data.get('content', instance.content)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

# 心理咨询聊天数据序列化器
class PsychologicalChatSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # ID，只读
    sender = serializers.ChoiceField(required=True, choices=['user', 'ai'])  # 发送人：user或ai
    content = serializers.CharField(required=True, max_length=1000)  # 发送内容，最大1000字符
    created_at = serializers.DateTimeField(read_only=True)  # 创建时间，只读
    
    def validate_content(self, value):
        """验证内容长度不超过1000个字符"""
        if len(value) > 1000:
            raise serializers.ValidationError("内容长度不能超过1000个字符")
        return value
    
    def create(self, validated_data):
        """创建新的心理咨询聊天记录"""
        return PsychologicalChat.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """更新现有心理咨询聊天记录"""
        instance.sender = validated_data.get('sender', instance.sender)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

# 心理知识子分类序列化器（递归结构）
class PsychologicalKnowledgeChildSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    content = serializers.CharField(required=True, max_length=500)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    childrens = serializers.SerializerMethodField()
    
    def get_childrens(self, obj):
        # 使用SerializerMethodField处理递归序列化
        if hasattr(obj, 'childrens') and obj.childrens:
            return PsychologicalKnowledgeChildSerializer(obj.childrens, many=True).data
        return []

# 心理知识主分类序列化器
class PsychologicalKnowledgeSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    content = serializers.CharField(required=True, max_length=500)
    childrens = serializers.ListField(
        child=PsychologicalKnowledgeChildSerializer(),
        required=False,
        default=list
    )
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """创建新的心理知识分类"""
        return PsychologicalKnowledge.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """更新现有心理知识分类"""
        instance.content = validated_data.get('content', instance.content)
        instance.childrens = validated_data.get('childrens', instance.childrens)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
