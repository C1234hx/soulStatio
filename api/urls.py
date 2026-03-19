from django.urls import path, re_path
from .views import UserList, UserDetail, ActionAdviceList, ActionAdviceDetail, ChickenSoupList, ChickenSoupDetail, ActionAdviceRandom, ChickenSoupRandom, PsychologicalChatList, PsychologicalKnowledgeMainList, PsychologicalKnowledgeDetailByParentId, WechatLogin, PsychologicalQnAList, PsychologicalQnADetail, UserMoodAnalysis

urlpatterns = [
    # 用户相关路由
    path('users/', UserList.as_view(), name='user-list'),
    re_path(r'^users/(?P<pk>[^/]+)/?$', UserDetail.as_view(), name='user-detail'),
    
    # 行动建议相关路由
    path('action-advice/', ActionAdviceList.as_view(), name='action-advice-list'),
    path('action-advice/random/', ActionAdviceRandom.as_view(), name='action-advice-random'),
    re_path(r'^action-advice/(?P<pk>[^/]+)/?$', ActionAdviceDetail.as_view(), name='action-advice-detail'),
    
    # 鸡汤数据相关路由
    path('chicken-soup/', ChickenSoupList.as_view(), name='chicken-soup-list'),
    path('chicken-soup/random/', ChickenSoupRandom.as_view(), name='chicken-soup-random'),
    re_path(r'^chicken-soup/(?P<pk>[^/]+)/?$', ChickenSoupDetail.as_view(), name='chicken-soup-detail'),
    
    # 心理咨询聊天数据路由
    path('psychological-chat/', PsychologicalChatList.as_view(), name='psychological-chat-list'),
    # 用户心情分析路由
    path('user-mood-analysis/', UserMoodAnalysis.as_view(), name='user-mood-analysis'),
    
    # 心理知识分类相关路由
    path('psychological-knowledge/main/', PsychologicalKnowledgeMainList.as_view(), name='psychological-knowledge-main-list'),
    re_path(r'^psychological-knowledge/detail/(?P<parent_id>[^/]+)/?$', PsychologicalKnowledgeDetailByParentId.as_view(), name='psychological-knowledge-detail-by-parent-id'),
    
    # 微信登录相关路由
    path('wechat/login/', WechatLogin.as_view(), name='wechat-login'),
    
    # 心理知识问答相关路由
    path('psychological-qna/', PsychologicalQnAList.as_view(), name='psychological-qna-list'),
    re_path(r'^psychological-qna/(?P<pk>[^/]+)/?$', PsychologicalQnADetail.as_view(), name='psychological-qna-detail'),
]
