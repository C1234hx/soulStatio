from django.urls import path
from .views import UserList, UserDetail, ActionAdviceList, ActionAdviceDetail

urlpatterns = [
    # 用户相关路由
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<str:pk>/', UserDetail.as_view(), name='user-detail'),
    
    # 行动建议相关路由
    path('action-advice/', ActionAdviceList.as_view(), name='action-advice-list'),
    path('action-advice/<str:pk>/', ActionAdviceDetail.as_view(), name='action-advice-detail'),
]
