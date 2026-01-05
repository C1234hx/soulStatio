from django.urls import path, re_path
from .views import UserList, UserDetail, ActionAdviceList, ActionAdviceDetail, ChickenSoupList, ChickenSoupDetail

urlpatterns = [
    # 用户相关路由
    path('users/', UserList.as_view(), name='user-list'),
    re_path(r'^users/(?P<pk>[^/]+)/?$', UserDetail.as_view(), name='user-detail'),
    
    # 行动建议相关路由
    path('action-advice/', ActionAdviceList.as_view(), name='action-advice-list'),
    re_path(r'^action-advice/(?P<pk>[^/]+)/?$', ActionAdviceDetail.as_view(), name='action-advice-detail'),
    
    # 鸡汤数据相关路由
    path('chicken-soup/', ChickenSoupList.as_view(), name='chicken-soup-list'),
    re_path(r'^chicken-soup/(?P<pk>[^/]+)/?$', ChickenSoupDetail.as_view(), name='chicken-soup-detail'),
]
