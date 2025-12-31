from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, ActionAdvice
from .serializers import UserSerializer, ActionAdviceSerializer

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    
    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ActionAdviceList(APIView):
    """行动建议列表视图 - 用于获取所有行动建议和创建新的行动建议"""
    
    def get(self, request):
        """获取行动建议列表，支持情绪向筛选和内容模糊搜索"""
        # 获取查询参数
        emotion_direction = request.query_params.get('emotion_direction')
        content = request.query_params.get('content')
        
        # 构建查询条件
        query = {}
        
        # 处理情绪向筛选
        if emotion_direction is not None:
            try:
                emotion_direction = int(emotion_direction)
                if emotion_direction != 0:  # 0表示查询全部，不需要添加筛选条件
                    query['emotion_direction'] = emotion_direction
            except ValueError:
                pass  # 忽略无效的情绪向参数
        
        # 执行基础查询
        action_advices = ActionAdvice.objects(**query)
        
        # 处理内容模糊搜索
        if content and content.strip():
            # 使用正则表达式进行模糊匹配
            from mongoengine.queryset.visitor import Q
            action_advices = action_advices.filter(Q(content__icontains=content.strip()))
        serializer = ActionAdviceSerializer(action_advices, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """创建新的行动建议"""
        serializer = ActionAdviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActionAdviceDetail(APIView):
    """行动建议详情视图 - 用于获取、更新和删除单个行动建议"""
    
    def get_object(self, pk):
        """根据ID获取行动建议对象"""
        try:
            return ActionAdvice.objects.get(pk=pk)
        except ActionAdvice.DoesNotExist:
            return None
    
    def get(self, request, pk):
        """获取单个行动建议的详情"""
        action_advice = self.get_object(pk)
        if action_advice is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ActionAdviceSerializer(action_advice)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """更新行动建议"""
        action_advice = self.get_object(pk)
        if action_advice is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ActionAdviceSerializer(action_advice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """删除行动建议"""
        action_advice = self.get_object(pk)
        if action_advice is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        action_advice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
