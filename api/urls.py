from django.urls import path, re_path
from .views import UserList, UserDetail, ActionAdviceList, ActionAdviceDetail, ChickenSoupList, ChickenSoupDetail, ActionAdviceRandom, ChickenSoupRandom, PsychologicalChatList, PsychologicalKnowledgeList, PsychologicalKnowledgeDetail

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
    
    # 心理知识分类相关路由
    path('psychological-knowledge/', PsychologicalKnowledgeList.as_view(), name='psychological-knowledge-list'),
    re_path(r'^psychological-knowledge/(?P<pk>[^/]+)/?$', PsychologicalKnowledgeDetail.as_view(), name='psychological-knowledge-detail'),
]
