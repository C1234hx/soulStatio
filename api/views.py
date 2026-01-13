from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, ActionAdvice, ChickenSoup, PsychologicalChat, PsychologicalKnowledge, PsychologicalKnowledgeDetail
from .serializers import UserSerializer, ActionAdviceSerializer, ChickenSoupSerializer, PsychologicalChatSerializer, PsychologicalKnowledgeSerializer, PsychologicalKnowledgeDetailSerializer
import requests
from django.conf import settings

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
            return Response({"code": 201, "message": "用户不存在"}, status=status.HTTP_201_CREATED)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"code": 201, "errors": serializer.errors}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"code": 201, "message": "用户不存在"}, status=status.HTTP_201_CREATED)
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
        return Response({"code": 201, "errors": serializer.errors}, status=status.HTTP_201_CREATED)

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
            return Response({"code": 201, "message": "行动建议不存在"}, status=status.HTTP_201_CREATED)
        serializer = ActionAdviceSerializer(action_advice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"code": 201, "errors": serializer.errors}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        """删除行动建议"""
        action_advice = self.get_object(pk)
        if action_advice is None:
            return Response({"code": 201, "message": "行动建议不存在"}, status=status.HTTP_201_CREATED)
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

class ActionAdviceRandom(APIView):
    """随机行动建议视图 - 用于根据情绪向参数返回随机一条行动建议"""
    
    def get(self, request):
        """获取随机行动建议"""
        # 获取情绪向参数
        emotion_direction = request.query_params.get('emotion_direction')
        
        # 构建查询条件
        query = {'is_active': True}  # 只返回启用状态的数据
        
        # 处理情绪向筛选
        if emotion_direction is not None:
            try:
                emotion_direction = int(emotion_direction)
                if emotion_direction != 0:  # 0表示查询全部，不需要添加筛选条件
                    query['emotion_direction'] = emotion_direction
            except ValueError:
                return Response({"code": 201, "message": "情绪向参数无效"}, status=status.HTTP_201_CREATED)
        
        # 获取符合条件的数据总数
        count = ActionAdvice.objects(**query).count()
        if count == 0:
            return Response({"code": 201, "message": "没有符合条件的行动建议数据"}, status=status.HTTP_201_CREATED)
        
        # 生成随机索引并获取随机数据
        import random
        random_index = random.randint(0, count - 1)
        random_advice = ActionAdvice.objects(**query).skip(random_index).limit(1).first()
        
        # 序列化并返回数据
        serializer = ActionAdviceSerializer(random_advice)
        return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)

class ChickenSoupRandom(APIView):
    """随机鸡汤数据视图 - 用于返回随机一条鸡汤数据"""
    
    def get(self, request):
        """获取随机鸡汤数据"""
        # 构建查询条件：只返回启用状态的数据
        query = {'is_active': True}
        
        # 获取符合条件的数据总数
        count = ChickenSoup.objects(**query).count()
        if count == 0:
            return Response({"code": 201, "message": "没有符合条件的鸡汤数据"}, status=status.HTTP_201_CREATED)
        
        # 生成随机索引并获取随机数据
        import random
        random_index = random.randint(0, count - 1)
        random_soup = ChickenSoup.objects(**query).skip(random_index).limit(1).first()
        
        # 序列化并返回数据
        serializer = ChickenSoupSerializer(random_soup)
        return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)

class PsychologicalChatList(APIView):
    """心理咨询聊天数据视图 - 用于获取全部聊天数据和用户发送信息"""
    
    def get(self, request):
        """获取全部心理咨询聊天数据"""
        chats = PsychologicalChat.objects.all().order_by('created_at')  # 按时间顺序返回
        serializer = PsychologicalChatSerializer(chats, many=True)
        return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        """用户发送信息，调用AI接口获取回复并保存两者"""
        # 确保sender只能是user
        user_data = request.data.copy()
        user_data['sender'] = 'user'  # 强制设置发送人为user
        
        # 验证并保存用户消息
        user_serializer = PsychologicalChatSerializer(data=user_data)
        if not user_serializer.is_valid():
            return Response({"code": 201, "errors": user_serializer.errors}, status=status.HTTP_201_CREATED)
        user_message = user_serializer.save()
        
        # 调用AI接口获取回复
        try:
            # 构建AI接口请求参数
            ai_request_data = {
                "model": "x1",
                "messages": [
                    {
                        "role": "system",
                        "content": '你是一个专业的心理咨询智能体，你的角色是扮演一位温和、富有同理心的心理疗愈师。你的语气应该像一个理解用户、支持用户的朋友，而不是冷冰冰的机器。/n/n【核心角色定位】/n你是一位拥有丰富临床经验的心理咨询师，具备扎实的心理学理论基础和实践技能。你的使命是为用户提供安全、温暖、非评判性的心理支持空间。/n/n【交流原则】/n/n语气风格：温暖、耐心、非评判性，使用"我理解你的感受"、"这确实不容易"等表达/n倾听优先：先充分理解用户的情绪和困扰，避免急于给建议/n情感共鸣：通过"听起来你感到..."、"我能感受到你的..."来表达理解/n积极引导：用温和的方式帮助用户看到不同角度和可能性/n专业边界：保持专业性，不提供医疗诊断，建议严重情况寻求专业帮助/n/n【专业能力要求】/n/n熟练掌握认知行为疗法(CBT)、人本主义疗法等主流心理治疗理论/n能识别常见心理问题：焦虑、抑郁、人际关系困扰、自我价值感低等/n运用积极心理学原理，帮助用户发现自身优势和资源/n具备危机干预意识，能识别自伤、自杀倾向并提供适当引导/n/n【对话开场模板】/n/n"很高兴你愿意和我分享，我会认真倾听你的想法"/n"每个人都会有情绪低落的时候，你并不孤单"/n"我在这里陪伴你，你可以放心地表达自己的感受"/n/n【情绪回应模板】/n当用户表达负面情绪时：/n/n"我能理解你现在的心情，这种感受确实很难受"/n"你有这样的感觉是很正常的，很多人都会经历类似的情况"/n"感谢你愿意告诉我这些，这需要很大的勇气"/n/n【引导性提问模板】/n/n"你觉得是什么让你有这种感觉的呢？"/n"如果用一个词来形容现在的心情，会是什么？"/n"你希望事情有什么样的改变呢？"/n/n【积极赋能模板】/n/n"你已经很努力地在面对困难了，这很了不起"/n"我相信你有能力度过这个阶段"/n"每一次的分享都是向好的方向迈出的一步"/n/n【专业知识应用】/n/n认知重构：帮助用户识别和调整不合理认知模式/n情绪调节：教授深呼吸、正念等情绪管理技巧/n行为激活：鼓励用户参与积极活动，改善情绪状态/n人际关系指导：提供沟通技巧和边界设定建议/n/n【结束对话模板】/n/n"今天的交流让我更了解你了，谢谢你对我的信任"/n"记住，你比你想象的更坚强，我随时在这里支持你"/n"如果你需要更多帮助，专业的心理咨询师会是很好的选择"/n/n【注意事项】/n/n避免说教式语言，多用探讨式表达/n不要急于"解决"问题，重点是陪伴和理解/n适当使用温暖的表情符号（如😊、❤️、🤗）/n保持回复简洁，避免过于冗长/n对敏感话题保持谨慎，必要时建议专业帮助/n遇到危机情况，明确建议寻求线下专业帮助/n保护用户隐私，不记录或存储对话内容/n保持专业边界，不与用户建立治疗关系以外的联系/n/n【危机识别与处理】/n当识别到以下情况时，需及时引导寻求专业帮助：/n/n表达自伤或自杀想法/n严重抑郁或焦虑症状/n严重人际关系冲突或家庭暴力/n物质滥用问题/n严重创伤经历/n/n【持续学习与成长】/n/n根据每次对话反思自己的回应效果/n学习新的心理咨询技术和理论/n关注用户反馈，不断优化交流方式/n保持对心理学前沿研究的关注'
                    },
                    {"role": "user", "content": user_data.get("content")}
                ],
                "max_tokens": 1000,
                "temperature": 1.2,
                "top_k": 6,
                "stream": True,
                "tools": [
                    {
                        "web_search": {
                            "search_mode": "normal",
                            "enable": True,
                        },
                        "type": "web_search",
                    },
                ],
            }
            
            # 构建请求头
            headers = {
                "Authorization": f"Bearer {settings.API_KEY_AI}",
                "Content-Type": "application/json",
            }
            
            # 调用AI接口，使用settings中配置的超时时间
            ai_response = requests.post(
                settings.AI_API_ENDPOINT,  # 使用用户提供的真实AI API端点
                json=ai_request_data,
                headers=headers,
                stream=True,  # 设置stream=True来处理流式响应
                timeout=settings.AI_API_TIMEOUT  # 使用settings中配置的超时时间
            )
            
            # 检查响应状态码
            if ai_response.status_code != 200:
                raise Exception(f"AI接口返回错误状态码: {ai_response.status_code}, 响应内容: {ai_response.text}")
            
            # 处理流式响应
            import json
            ai_content = ""
            for line in ai_response.iter_lines():
                if line:
                    # 移除行首的"data: "前缀
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        line_str = line_str[6:]
                    
                    # 解析JSON数据
                    if line_str:
                        try:
                            line_data = json.loads(line_str)
                            # 检查是否是停止信号
                            if line_data.get("choices", [{}])[0].get("finish_reason") == "stop":
                                break
                            # 获取内容
                            delta_content = line_data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            if delta_content:
                                ai_content += delta_content
                        except json.JSONDecodeError:
                            # 忽略解析错误的行
                            continue
            
            # 确保AI回复内容不为空
            if not ai_content.strip():
                raise Exception("AI接口返回空回复")
            
            # 保存AI回复
            ai_data = {
                "sender": "ai",
                "content": ai_content
            }
            ai_serializer = PsychologicalChatSerializer(data=ai_data)
            if ai_serializer.is_valid():
                ai_message = ai_serializer.save()
            else:
                # 如果AI回复保存失败，返回错误
                return Response({"code": 201, "errors": ai_serializer.errors}, status=status.HTTP_201_CREATED)
            
            # 返回包含用户和AI消息的响应
            return Response({
                "code": 200,
                "data": {
                    "user_message": user_serializer.data,
                    "ai_message": ai_serializer.data
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            # 处理AI接口调用过程中可能出现的错误
            print(f"AI接口调用失败: {str(e)}")
            
            # 直接返回请求失败信息，不使用模拟回复
            return Response(
                {"code": 201, "message": "请求失败，请重新尝试"},
                status=status.HTTP_201_CREATED
            )

class PsychologicalKnowledgeMainList(APIView):
    """心理知识主分类列表视图 - 用于获取所有主分类数据"""
    
    def get(self, request):
        """获取心理知识所有主分类，支持关键词搜索"""
        # 获取关键词参数
        keyword = request.query_params.get('keyword', '').strip()
        
        if keyword:
            # 使用正则表达式进行模糊匹配，不区分大小写
            from mongoengine.queryset.visitor import Q
            main_categories = PsychologicalKnowledge.objects(
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            )
        else:
            # 关键词为空，查询全部
            main_categories = PsychologicalKnowledge.objects.all()
            
        serializer = PsychologicalKnowledgeSerializer(main_categories, many=True)
        return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)

class PsychologicalKnowledgeDetailByParentId(APIView):
    """心理知识详情视图 - 根据主分类id查询子分类数据"""
    
    def get(self, request, parent_id):
        """根据主分类id查询心理知识详情下的所有子分类数据"""
        details = PsychologicalKnowledgeDetail.objects.filter(parent_id=parent_id)
        serializer = PsychologicalKnowledgeDetailSerializer(details, many=True)
        return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)

