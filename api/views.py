from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, ActionAdvice, ChickenSoup, PsychologicalChat, PsychologicalKnowledge, PsychologicalKnowledgeDetail, PsychologicalQnA
from .serializers import UserSerializer, ActionAdviceSerializer, ChickenSoupSerializer, PsychologicalChatSerializer, PsychologicalKnowledgeSerializer, PsychologicalKnowledgeDetailSerializer, PsychologicalQnASerializer
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import jwt
import time
from django.conf import settings

# 情感词词典 - 用于心理数据分析的关键词统计
EMOTION_WORDS = {
    # 负面情绪词
    '烦', '烦恼', '烦躁', '郁闷', '不开心', '难过', '伤心', '痛苦', '悲伤', '压抑',
    '焦虑', '焦虑不安', '紧张', '不安', '害怕', '恐惧', '担忧', '担心', '忧虑',
    '生气', '愤怒', '暴躁', '烦躁不安', '气愤', '不满', '失望', '绝望', '灰心',
    '孤单', '孤独', '寂寞', '无助', '无奈', '迷茫', '困惑', '纠结', '矛盾',
    '自卑', '自责', '愧疚', '后悔', '悔恨', '沮丧', '失落', '低落', '消沉',
    '疲惫', '累', '疲倦', '倦怠', '心力交瘁', '身心俱疲',

    # 正面情绪词
    '开心', '高兴', '快乐', '愉快', '幸福', '满足', '满意', '欣慰', '安心',
    '平静', '放松', '舒适', '自在', '宁静', '舒服', '开心', '喜悦', '愉悦',
    '希望', '乐观', '积极', '兴奋', '激动', '感激', '感谢', '感动', '温暖',
    '自信', '骄傲', '自豪', '坚强', '勇敢', '坚定', '有力量', '有希望',

    # 中性但心理相关词
    '想', '思考', '想想', '思考一下', '觉得', '感觉', '感到', '认为',
    '需要', '想要', '希望', '期望', '期待',
    '爱', '喜欢', '爱你', '想念', '思念',
    '睡不着', '失眠', '睡眠', '困', '想睡',
    '压力', '压力大', '有压力',
    '工作', '学习', '生活', '感情', '家庭', '朋友', '人际关系'
}

# 会话管理类，优化连接池使用
class SessionManager:
    _session = None
    
    @classmethod
    def get_session(cls):
        if cls._session is None:
            # 创建会话，配置连接池
            cls._session = requests.Session()
            # 配置重试策略
            retries = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504]
            )
            # 配置连接池
            adapter = HTTPAdapter(
                pool_connections=10,
                pool_maxsize=10,
                max_retries=retries
            )
            # 应用到所有HTTP/HTTPS请求
            cls._session.mount('http://', adapter)
            cls._session.mount('https://', adapter)
        return cls._session

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
        # 按时间倒序获取聊天记录
        chats = PsychologicalChat.objects.all().order_by('-created_at')  # 按时间倒序返回
        
        # 确保AI回复在用户问题下方（用户问题在前，AI回复在后）
        # 对结果进行重新排序，确保每个用户消息后面跟着对应的AI消息
        sorted_chats = []
        
        # 按时间倒序遍历，确保最新的对话在前面
        i = 0
        while i < len(chats):
            # 检查当前消息是否为AI回复
            if chats[i].sender == 'ai' and i + 1 < len(chats) and chats[i+1].sender == 'user':
                # 如果当前是AI回复，且下一条是用户消息，交换顺序
                sorted_chats.append(chats[i+1])  # 用户消息在前
                sorted_chats.append(chats[i])    # AI回复在后
                i += 2
            else:
                # 其他情况直接添加
                sorted_chats.append(chats[i])
                i += 1
        
        # 序列化并返回
        serializer = PsychologicalChatSerializer(sorted_chats, many=True)
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
        
        # 获取今日历史用户消息，随机抽取2条
        import random
        from datetime import datetime
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_user_messages = list(PsychologicalChat.objects(
            created_at__gte=today_start,
            sender='user'
        ).only('content'))  # 只查询content字段
        
        # 随机抽取2条历史消息（排除刚发送的这条）
        history_messages = []
        if len(today_user_messages) > 1:
            # 排除刚保存的消息（最后一条）
            recent_msg_id = str(user_message.id)
            available_messages = [msg for msg in today_user_messages if str(msg.id) != recent_msg_id]
            if len(available_messages) >= 2:
                history_messages = random.sample(available_messages, 2)
            elif len(available_messages) == 1:
                history_messages = [available_messages[0]]
        
        # 构建带历史上下文的用户消息
        user_content = user_data.get("content")
        if history_messages:
            history_context = "\n\n【历史对话】："
            for i, hist_msg in enumerate(history_messages, 1):
                history_context += f"\n{i}. {hist_msg.content}"
            user_content += history_context
        
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
                    {"role": "user", "content": user_content}
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
            
            # 使用会话管理类获取会话
            session = SessionManager.get_session()
            
            # 调用AI接口，使用settings中配置的超时时间
            ai_response = session.post(
                settings.AI_API_ENDPOINT,  # 使用用户提供的真实AI API端点
                json=ai_request_data,
                headers=headers,
                stream=True,  # 设置stream=True来处理流式响应
                timeout=settings.AI_API_TIMEOUT  # 使用settings中配置的超时时间
            )
            
            try:
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
            finally:
                ai_response.close()  # 确保响应被关闭
            
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

class UserMoodAnalysis(APIView):
    """用户心情分析视图 - 用于获取7日内心情指数和今日关键词"""
    
    def get(self, request):
        """获取7日内心情指数和今日关键词"""
        try:
            from datetime import datetime, timedelta
            import re
            from collections import Counter
            import requests
            
            # 计算7天前的日期
            today = datetime.now()
            seven_days_ago = today - timedelta(days=6)
            
            # 1. 计算7日内心情指数
            mood_data = []
            for i in range(7):
                current_date = seven_days_ago + timedelta(days=i)
                date_str = current_date.strftime("%m/%d")
                
                # 获取当天的聊天记录
                start_of_day = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_of_day = current_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                
                # 直接查询用户消息，使用only方法只查询需要的字段
                user_messages = PsychologicalChat.objects(
                    created_at__gte=start_of_day,
                    created_at__lte=end_of_day,
                    sender='user'
                ).only('content')  # 只查询content字段，避免查询sentiment_score
                
                message_count = user_messages.count()
                
                if message_count == 0:
                    mood_value = 50  # 无消息默认值
                else:
                    # 合并所有用户消息为一个文本
                    all_content = " ".join(chat.content for chat in user_messages)
                    
                    # 尝试使用百度情感分析API
                    try:
                        # 获取百度API token
                        API_KEY = "xpVdKMZPqXwcbESkQmJcGqj5"
                        SECRET_KEY = "82v8U8qgGWG247ltw4pFuOrQUVsElT7n"
                        token_url = "https://aip.baidubce.com/oauth/2.0/token"
                        token_params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
                        
                        token_response = requests.post(token_url, params=token_params, timeout=10)
                        try:
                            token_data = token_response.json()
                            access_token = token_data.get("access_token")
                            
                            if access_token:
                                # 调用情感分析API
                                sentiment_url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token={access_token}"
                                payload = {"text": all_content}
                                headers = {
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json'
                                }
                                
                                sentiment_response = requests.post(sentiment_url, headers=headers, json=payload, timeout=15)
                                try:
                                    sentiment_data = sentiment_response.json()
                                    
                                    if "items" in sentiment_data and sentiment_data["items"]:
                                        positive_prob = sentiment_data["items"][0].get("positive_prob", 0.5)
                                        mood_value = int(positive_prob * 100)
                                    else:
                                        mood_value = 50  # 默认值
                                finally:
                                    sentiment_response.close()
                            else:
                                mood_value = 50  # 默认值
                        finally:
                            token_response.close()
                    except Exception as api_error:
                        print(f"百度情感分析API调用失败: {str(api_error)}")
                        mood_value = 50  # 失败时使用默认值
                
                mood_data.append({"date": date_str, "value": mood_value})
            
            # 2. 提取今日关键词（基于情感词词典）
            today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
            today_chats = PsychologicalChat.objects(
                created_at__gte=today_start,
                sender='user'
            ).only('content')  # 只查询content字段
            
            # 统计情感词出现次数（优先匹配长词，避免重复计数）
            emotion_word_counts = Counter()
            
            # 按词长度从长到短排序，优先匹配长词
            sorted_words = sorted(EMOTION_WORDS, key=len, reverse=True)
            
            for chat in today_chats:
                content = chat.content
                matched_words = set()  # 记录已匹配的词，避免重复
                
                # 检查每个情感词（从长到短）是否在内容中
                for word in sorted_words:
                    if word in content:
                        # 检查这个词是否已经被更长的词包含
                        already_matched = False
                        for matched_word in matched_words:
                            if word in matched_word:
                                already_matched = True
                                break
                        
                        if not already_matched:
                            matched_words.add(word)
                
                # 统计匹配到的词
                for word in matched_words:
                    emotion_word_counts[word] += 1
            
            # 取前5个情感词作为今日关键词
            top_keywords = [
                {"word": word, "count": count}
                for word, count in emotion_word_counts.most_common(5)
            ]
            
            # 构建返回数据
            return Response({
                "code": 200,
                "data": {
                    "mood_data": mood_data,
                    "keywords": top_keywords
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"心情分析失败: {str(e)}")
            return Response(
                {"code": 201, "message": "获取心情分析数据失败"},
                status=status.HTTP_201_CREATED
            )

class WechatLogin(APIView):
    """微信登录视图 - 处理微信小程序登录逻辑"""
    
    def post(self, request):
        """处理微信登录请求"""
        # 获取前端发送的code
        code = request.data.get('code')
        if not code:
            return Response({"code": 201, "message": "缺少code参数"}, status=status.HTTP_201_CREATED)
        
        # 获取前端发送的用户信息
        nickname = request.data.get('nickname', '微信用户')
        avatar = request.data.get('avatar', '')
        
        try:
            # 调用微信官方API获取openid和session_key
            appid = 'wxc2e5a8111bf8c8ee'  # 替换为你的微信小程序appid
            secret = '452aa98fcc5fdf5957a1af4e62c47bce'  # 替换为你的微信小程序secret
            url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            # 检查是否获取成功
            if 'openid' not in data:
                return Response({"code": 201, "message": f"获取openid失败: {data.get('errmsg', '未知错误')}"}, status=status.HTTP_201_CREATED)
            
            openid = data['openid']
            session_key = data.get('session_key')
            
            # 检查用户是否已存在
            try:
                user = User.objects.get(openid=openid)
                # 更新用户信息
                user.nickname = nickname
                user.avatar = avatar
                user.save()
            except User.DoesNotExist:
                # 创建新用户
                user = User(
                    openid=openid,
                    nickname=nickname,
                    avatar=avatar,
                    is_admin=False
                )
                user.save()
            
            # 生成JWT token
            payload = {
                'user_id': str(user.id),
                'openid': openid,
                'exp': time.time() + 86400 * 7  # 7天过期
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            
            # 返回用户信息和token
            return Response({
                "code": 200,
                "data": {
                    "token": token,
                    "user_info": {
                        "avatar": user.avatar,
                        "nickname": user.nickname,
                        "is_admin": user.is_admin
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"微信登录失败: {str(e)}")
            return Response({"code": 201, "message": "登录失败，请重试"}, status=status.HTTP_201_CREATED)

class PsychologicalQnAList(APIView):
    """心理知识问答列表视图 - 用于获取所有问答数据和用户发送信息"""
    
    def get(self, request):
        """获取心理知识问答列表，支持分类筛选和关键词搜索"""
        # 获取查询参数
        category = request.query_params.get('category')
        keyword = request.query_params.get('keyword')
        
        # 构建查询条件
        query = {'is_active': True}  # 只返回启用状态的数据
        
        # 处理分类筛选
        if category and category.strip():
            query['category'] = category.strip()
        
        # 执行基础查询，按时间倒序排列
        qnas = PsychologicalQnA.objects(**query).order_by('-created_at')
        
        # 处理关键词搜索
        if keyword and keyword.strip():
            # 使用正则表达式进行模糊匹配
            from mongoengine.queryset.visitor import Q
            qnas = qnas.filter(Q(question__icontains=keyword.strip()) | Q(answer__icontains=keyword.strip()))
        
        # 转换为和心理咨询API一样的格式
        result = []
        for qna in qnas:
            # 添加用户消息
            result.append({
                "id": str(qna.id),
                "sender": "user",
                "content": qna.question,
                "created_at": qna.created_at.isoformat().replace('+00:00', 'Z')
            })
            # 添加AI消息（确保在用户问题下方）
            result.append({
                "id": str(qna.id),
                "sender": "ai",
                "content": qna.answer,
                "created_at": qna.created_at.isoformat().replace('+00:00', 'Z')
            })
        
        return Response({"code": 200, "data": result}, status=status.HTTP_200_OK)
    
    def post(self, request):
        """用户发送信息，调用本地Ollama模型获取回复并保存到心理知识问答表"""
        # 确保sender只能是user
        user_data = request.data.copy()
        user_data['sender'] = 'user'  # 强制设置发送人为user
        
        # 验证并保存用户消息（不保存到数据库，只用于返回格式）
        user_serializer = PsychologicalChatSerializer(data=user_data)
        if not user_serializer.is_valid():
            return Response({"code": 201, "errors": user_serializer.errors}, status=status.HTTP_201_CREATED)
        
        # 调用Dify本地模型获取回复
        try:
            # 构建Dify API请求参数（兼容OpenAI格式）
            dify_request_data = {
                "model": "deepseek-r1:7b",
                "messages": [
                    {
                        "role": "system",
                        "content": ""
                    },
                    {
                        "role": "user",
                        "content": user_data.get("content")
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            # 构建请求头
            headers = {
                "Authorization": f"Bearer {settings.DIFY_API_KEY}",
                "Content-Type": "application/json",
            }
            
            # 使用会话管理类获取会话
            session = SessionManager.get_session()
            
            # 调用Dify API
            dify_response = session.post(
                f"{settings.DIFY_API_ENDPOINT}/chat-messages",
                json={
                    "inputs": {},
                    "query": user_data.get("content"),
                    "response_mode": "blocking",
                    "conversation_id": "",
                    "user": "psy_user"
                },
                headers=headers,
                timeout=settings.AI_API_TIMEOUT
            )
            
            try:
                # 检查响应状态码
                if dify_response.status_code != 200:
                    raise Exception(f"Dify API返回错误状态码: {dify_response.status_code}, 响应内容: {dify_response.text}")
                
                # 解析响应（Dify API格式）
                response_data = dify_response.json()
                ai_content = response_data.get("answer", "").strip()
                
                # 打印原始内容用于调试
                print(f"原始AI回复: {repr(ai_content)}")
                
                # 去除思考部分（移除 <think>...</think> 标签及其内容）
                import re
                # 匹配不同格式的think标签（包括可能的空格和转义）
                # 使用 re.DOTALL 确保 . 能匹配换行符
                ai_content = re.sub(r'<think[\s\S]*?</think>', '', ai_content, flags=re.IGNORECASE | re.DOTALL).strip()
                # 再次检查是否还有残留的think标签
                ai_content = re.sub(r'<think\s*>', '', ai_content, flags=re.IGNORECASE).strip()
                ai_content = re.sub(r'</think\s*>', '', ai_content, flags=re.IGNORECASE).strip()
                
                # 打印处理后的内容用于调试
                print(f"处理后AI回复: {repr(ai_content)}")
                
            finally:
                dify_response.close()  # 确保响应被关闭
            
            # 确保AI回复内容不为空
            if not ai_content:
                raise Exception("Dify模型返回空回复")
            
            # 保存到心理知识问答表
            qna_data = {
                "question": user_data.get("content"),
                "answer": ai_content,
                "category": "默认分类"
            }
            qna_serializer = PsychologicalQnASerializer(data=qna_data)
            if not qna_serializer.is_valid():
                return Response({"code": 201, "errors": qna_serializer.errors}, status=status.HTTP_201_CREATED)
            qna_message = qna_serializer.save()
            
            # 构造返回数据（和心理咨询API一样的格式）
            user_message = {
                "id": str(qna_message.id),
                "sender": "user",
                "content": user_data.get("content"),
                "created_at": qna_message.created_at.isoformat().replace('+00:00', 'Z')
            }
            
            ai_message = {
                "id": str(qna_message.id),
                "sender": "ai",
                "content": ai_content,
                "created_at": qna_message.created_at.isoformat().replace('+00:00', 'Z')
            }
            
            # 返回包含用户和AI消息的响应
            return Response({
                "code": 200,
                "data": {
                    "user_message": user_message,
                    "ai_message": ai_message
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            # 处理AI接口调用过程中可能出现的错误
            print(f"Dify模型调用失败: {str(e)}")
            
            # 直接返回请求失败信息，不使用模拟回复
            return Response(
                {"code": 201, "message": "请求失败，请重新尝试"},
                status=status.HTTP_201_CREATED
            )

class PsychologicalQnADetail(APIView):
    """心理知识问答详情视图 - 用于获取、更新和删除单个问答数据"""
    
    def get_object(self, pk):
        """根据ID获取心理知识问答对象"""
        try:
            return PsychologicalQnA.objects.get(pk=pk)
        except PsychologicalQnA.DoesNotExist:
            return None
    
    def get(self, request, pk):
        """获取单个心理知识问答的详情，返回格式和心理咨询API一样"""
        qna = self.get_object(pk)
        if qna is None:
            return Response({"code": 201, "message": "心理知识问答不存在"}, status=status.HTTP_201_CREATED)
        
        # 构造返回数据（和心理咨询API一样的格式）
        user_message = {
            "id": str(qna.id),
            "sender": "user",
            "content": qna.question,
            "created_at": qna.created_at.isoformat().replace('+00:00', 'Z')
        }
        
        ai_message = {
            "id": str(qna.id),
            "sender": "ai",
            "content": qna.answer,
            "created_at": qna.created_at.isoformat().replace('+00:00', 'Z')
        }
        
        return Response({
            "code": 200,
            "data": {
                "user_message": user_message,
                "ai_message": ai_message
            }
        }, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        """更新心理知识问答"""
        qna = self.get_object(pk)
        if qna is None:
            return Response({"code": 201, "message": "心理知识问答不存在"}, status=status.HTTP_201_CREATED)
        serializer = PsychologicalQnASerializer(qna, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"code": 201, "errors": serializer.errors}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        """删除心理知识问答"""
        qna = self.get_object(pk)
        if qna is None:
            return Response({"code": 201, "message": "心理知识问答不存在"}, status=status.HTTP_201_CREATED)
        qna.delete()
        return Response({"code": 200, "message": "删除成功"}, status=status.HTTP_200_OK)

