from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, ActionAdvice, ChickenSoup
from .serializers import UserSerializer, ActionAdviceSerializer, ChickenSoupSerializer

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"code": 201, "errors": serializer.errors}, status=status.HTTP_201_CREATED)

class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    
    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"code": 201, "message": "用户不存在"}, status=status.HTTP_201_CREATED)
        serializer = UserSerializer(user)
        return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"code": 1, "message": "用户不存在"}, status=status.HTTP_201_CREATED)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"code": 1, "errors": serializer.errors}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"code": 1, "message": "用户不存在"}, status=status.HTTP_200_OK)
        user.delete()
        return Response({"code": 200, "message": "删除成功"}, status=status.HTTP_200_OK)

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
        return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        """创建新的行动建议"""
        serializer = ActionAdviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"code": 1, "errors": serializer.errors}, status=status.HTTP_200_OK)

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
            return Response({"code": 201, "message": "行动建议不存在"}, status=status.HTTP_201_CREATED)
        serializer = ActionAdviceSerializer(action_advice)
        return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        """更新行动建议"""
        action_advice = self.get_object(pk)
        if action_advice is None:
            return Response({"code": 1, "message": "行动建议不存在"}, status=status.HTTP_200_OK)
        serializer = ActionAdviceSerializer(action_advice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"code": 1, "errors": serializer.errors}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        """删除行动建议"""
        action_advice = self.get_object(pk)
        if action_advice is None:
            return Response({"code": 1, "message": "行动建议不存在"}, status=status.HTTP_200_OK)
        action_advice.delete()
        return Response({"code": 200, "message": "删除成功"}, status=status.HTTP_200_OK)

class ChickenSoupList(APIView):
    """鸡汤数据列表视图 - 用于获取所有鸡汤数据和创建新的鸡汤数据"""
    
    def get(self, request):
        """获取全部鸡汤数据"""
        chicken_soups = ChickenSoup.objects.all()
        serializer = ChickenSoupSerializer(chicken_soups, many=True)
        return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        """创建新的鸡汤数据"""
        serializer = ChickenSoupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"code": 201, "errors": serializer.errors}, status=status.HTTP_201_CREATED)

class ChickenSoupDetail(APIView):
    """鸡汤数据详情视图 - 用于删除单个鸡汤数据"""
    
    def get_object(self, pk):
        """根据ID获取鸡汤数据对象"""
        try:
            return ChickenSoup.objects.get(pk=pk)
        except ChickenSoup.DoesNotExist:
            return None
    
    def delete(self, request, pk):
        """删除鸡汤数据"""
        chicken_soup = self.get_object(pk)
        if chicken_soup is None:
            return Response({"code": 201, "message": "鸡汤数据不存在"}, status=status.HTTP_201_CREATED)
        chicken_soup.delete()
        return Response({"code": 200, "message": "删除成功"}, status=status.HTTP_200_OK)
