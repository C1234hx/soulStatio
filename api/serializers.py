from rest_framework import serializers
from .models import User

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
