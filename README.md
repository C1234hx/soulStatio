# Django + MongoDB 后端开发新手教程

## 🎯 项目概述

这是一个基于 **Django 6.0** 和 **MongoDB** 的后端项目，采用**前后端分离**架构，为前端应用（如微信小程序）提供 RESTful API 接口。

### 核心功能
- ✅ 使用 Django REST Framework 构建 RESTful API
- ✅ 连接 MongoDB 数据库存储数据
- ✅ 支持跨域请求（CORS）
- ✅ 提供用户数据的增删改查接口

### 技术栈
| 技术/库 | 版本 | 用途 |
|---------|------|------|
| Python | 3.10+ | 编程语言 |
| Django | 6.0 | Web 框架 |
| Django REST Framework | 3.15+ | REST API 开发 |
| mongoengine | 0.28+ | MongoDB 数据库驱动 |
| django-cors-headers | 4.4+ | 跨域请求支持 |

## 🚀 环境搭建

### 1. 安装 Python
- 下载并安装 Python 3.10 或更高版本：https://www.python.org/downloads/
- 安装时勾选 "Add Python to PATH"

### 2. 创建虚拟环境
打开命令行（CMD 或 PowerShell）：

```powershell
# 进入项目目录
cd C:\Users\EDY\Desktop\soulStation

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\activate
```

### 3. 安装依赖

```powershell
# 安装核心依赖
pip install django==6.0 djangorestframework mongoengine django-cors-headers

# 安装测试工具（可选）
pip install requests
```

## 📁 项目结构

```
soulStation/
├── soulStation/          # 项目主目录
│   ├── __init__.py       # 项目初始化文件
│   ├── settings.py       # 项目配置文件（非常重要！）
│   ├── urls.py           # 主 URL 配置
│   └── wsgi.py           # WSGI 服务器配置
├── api/                  # API 应用目录
│   ├── __init__.py       # 应用初始化文件
│   ├── admin.py          # 后台管理配置
│   ├── models.py         # 数据模型定义
│   ├── serializers.py    # 数据序列化器
│   ├── views.py          # API 视图函数
│   └── urls.py           # API 路由配置
├── .venv/                # 虚拟环境目录
├── manage.py             # Django 管理工具
└── README.md             # 项目说明文档
```

## 📊 MongoDB 数据库配置

### 1. 安装 MongoDB
- 下载并安装 MongoDB Community Server：https://www.mongodb.com/try/download/community
- 安装时选择 "Complete" 完全安装

### 2. 启动 MongoDB 服务

#### 方法 1：通过 Windows 服务
- 按 `Win + R` 打开运行窗口，输入 `services.msc`
- 找到 "MongoDB Server" 服务
- 右键点击 "启动"，也可以设置为 "自动" 启动

#### 方法 2：通过命令行
```powershell
# 启动 MongoDB 服务
net start MongoDB

# 停止 MongoDB 服务
net stop MongoDB
```

### 3. 配置 Django 连接 MongoDB

打开 `soulStation/settings.py` 文件，修改以下内容：

#### 步骤 1：添加应用
找到 `INSTALLED_APPS` 列表，添加以下内容：

```python
INSTALLED_APPS = [
    # ... 其他应用 ...
    'rest_framework',       # Django REST Framework
    'corsheaders',          # 跨域支持
    'api',                  # 我们的 API 应用
]
```

#### 步骤 2：添加中间件
找到 `MIDDLEWARE` 列表，添加 CORS 中间件（放在最前面）：

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS 中间件
    # ... 其他中间件 ...
]
```

#### 步骤 3：配置 CORS
在文件末尾添加：

```python
# 允许所有跨域请求（开发阶段使用）
CORS_ALLOW_ALL_ORIGINS = True
```

#### 步骤 4：配置 MongoDB 连接
在文件末尾添加：

```python
# MongoDB 连接配置
MONGODB_SETTINGS = {
    'db': 'soulstation_db',    # 数据库名称
    'host': 'localhost',       # 主机地址
    'port': 27017,             # 端口号
    # 如果启用了 MongoDB 认证，添加以下两行
    'username': 'your_username',
    'password': 'your_password',
}
```

#### 步骤 5：初始化 MongoDB 连接
创建 `soulStation/mongodb.py` 文件：

```python
# soulStation/mongodb.py
from mongoengine import connect
from django.conf import settings

# 连接 MongoDB 数据库
connect(
    db=settings.MONGODB_SETTINGS['db'],
    host=settings.MONGODB_SETTINGS['host'],
    port=settings.MONGODB_SETTINGS['port'],
    # 如果启用了认证，添加以下参数
    username=settings.MONGODB_SETTINGS.get('username'),
    password=settings.MONGODB_SETTINGS.get('password'),
)
```

然后在 `soulStation/__init__.py` 中添加：

```python
# soulStation/__init__.py
# 导入 mongodb 模块，初始化数据库连接
import mongodb
```

## 🛠️ 接口开发（以用户模块为例）

### 1. 定义数据模型（Models）

打开 `api/models.py` 文件，定义用户数据模型：

```python
# api/models.py
from mongoengine import Document, StringField, IntField, DateTimeField
from datetime import datetime

# 用户数据模型
class User(Document):
    username = StringField(required=True, unique=True, max_length=50)  # 用户名
    email = StringField(required=True, unique=True, max_length=100)     # 邮箱
    age = IntField(min_value=0, max_value=150, required=False)          # 年龄
    created_at = DateTimeField(default=datetime.now)                    # 创建时间
    updated_at = DateTimeField(default=datetime.now)                    # 更新时间
    
    meta = {
        'collection': 'users',     # MongoDB 集合名称
        'ordering': ['-created_at'] # 排序方式：按创建时间倒序
    }
```

### 2. 创建序列化器（Serializers）

序列化器用于将 Python 对象转换为 JSON 格式，便于网络传输。

打开 `api/serializers.py` 文件：

```python
# api/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # 只读字段
    username = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True, max_length=100)
    age = serializers.IntegerField(min_value=0, max_value=150, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        """创建新用户"""
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """更新用户信息"""
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance
```

### 3. 编写视图（Views）

视图用于处理 HTTP 请求并返回响应。

打开 `api/views.py` 文件：

```python
# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

# 用户列表视图（获取所有用户，创建新用户）
class UserList(APIView):
    def get(self, request):
        """获取所有用户"""
        users = User.objects.all()#用户的所有字段
        serializer = UserSerializer(users, many=True)#获取模型的所有字段
        return Response(serializer.data)
    
    def post(self, request):
        """创建新用户"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() #内置方法应该是，保存这条传入的数据
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 用户详情视图（获取、更新、删除单个用户）
class UserDetail(APIView):
    def get_object(self, pk):
        """获取指定 ID 的用户"""
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    
    def get(self, request, pk):
        """获取单个用户详情"""
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """更新用户信息"""
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """删除用户"""
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### 4. 配置 URL 路由

#### 步骤 1：配置 API 应用的路由

打开 `api/urls.py` 文件：

```python
# api/urls.py
from django.urls import path
from .views import UserList, UserDetail

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),       # 获取所有用户、创建用户
    path('users/<str:pk>/', UserDetail.as_view(), name='user-detail'),  # 获取、更新、删除单个用户
]
```

#### 步骤 2：配置项目主路由

打开 `soulStation/urls.py` 文件：

```python
# soulStation/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),       # 后台管理
    path('api/', include('api.urls')),     # 包含 API 应用的路由
]
```

## 💾 数据库操作

### 1. 创建 MongoDB 数据库和集合

无需手动创建！当您第一次向数据库添加数据时，MongoDB 会自动创建数据库和集合。

### 2. 常用数据库操作

Django REST Framework 已经帮我们实现了所有的数据库操作接口，您可以通过 HTTP 请求来操作数据：

| 请求方法 | URL | 功能 |
|----------|-----|------|
| GET | http://localhost:8000/api/users/ | 获取所有用户 |
| POST | http://localhost:8000/api/users/ | 创建新用户 |
| GET | http://localhost:8000/api/users/{id}/ | 获取单个用户详情 |
| PUT | http://localhost:8000/api/users/{id}/ | 更新用户信息 |
| DELETE | http://localhost:8000/api/users/{id}/ | 删除用户 |

### 3. 使用 Navicat 可视化管理数据

1. 打开 Navicat
2. 创建新连接 → MongoDB
3. 主机：localhost，端口：27017
4. **取消勾选** "启用认证"（开发阶段）
5. 点击 "测试连接"，成功后保存
6. 连接后可以看到 `soulstation_db` 数据库和 `users` 集合

## 🎉 启动服务

### 1. 初始化数据库

```powershell
# 激活虚拟环境（如果没有激活）
.venv\Scripts\activate

# 进入项目目录
cd C:\Users\EDY\Desktop\soulStation

# 生成数据库迁移文件
python manage.py makemigrations

# 执行数据库迁移
python manage.py migrate
```

### 2. 启动开发服务器

```powershell
# 启动 Django 开发服务器
python manage.py runserver
```

服务启动后，您可以在浏览器中访问：
- 管理后台：http://localhost:8000/admin/（需要创建超级用户）
- API 接口：http://localhost:8000/api/users/

### 3. 测试接口

您可以使用以下工具测试 API 接口：

#### 方法 1：使用浏览器
直接访问 `http://localhost:8000/api/users/` 可以查看所有用户。

#### 方法 2：使用 `test_api.py` 脚本

项目中提供了一个测试脚本：

```powershell
# 安装 requests 库（如果未安装）
pip install requests

# 运行测试脚本
python test_api.py
```

#### 方法 3：使用 Postman

1. 下载并安装 Postman：https://www.postman.com/downloads/
2. 创建新请求：
   - 方法：POST
   - URL：http://localhost:8000/api/users/
   - Body → raw → JSON
   - 输入：
     ```json
     {
       "username": "testuser",
       "email": "test@example.com",
       "age": 20
     }
     ```
3. 点击 "Send"，查看响应

## 🔗 前端调用示例（微信小程序）

以下是微信小程序中使用 `uni.request` 调用 API 的示例：

```javascript
// 获取所有用户
try {
  const res = await uni.request({
    url: 'http://localhost:8000/api/users/',
    method: 'GET'
  });
  console.log('用户列表:', res.data);
} catch (error) {
  console.error('请求失败:', error);
}

// 创建新用户
try {
  const res = await uni.request({
    url: 'http://localhost:8000/api/users/',
    method: 'POST',
    data: {
      username: 'wechat_user',
      email: 'wechat@example.com',
      age: 25
    }
  });
  console.log('创建成功:', res.data);
} catch (error) {
  console.error('请求失败:', error);
}
```

### 微信小程序开发注意事项

1. 在开发阶段，需要在小程序开发者工具中：
   - 点击右上角 "详情" → "本地设置"
   - 勾选 "不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书"

2. 生产环境需要：
   - 配置 HTTPS 域名
   - 在微信公众平台添加合法域名

## ❌ 常见问题及解决方案

### 1. 数据库连接失败

**错误信息**：`Could not connect to MongoDB`

**解决方法**：
- 检查 MongoDB 服务是否正在运行
- 确认 `settings.py` 中的 `MONGODB_SETTINGS` 配置正确
- 确保 MongoDB 端口 27017 没有被占用

### 2. 跨域请求失败

**错误信息**：`Access-Control-Allow-Origin` 相关错误

**解决方法**：
- 检查 `settings.py` 中是否添加了 `corsheaders.middleware.CorsMiddleware`
- 确认 `CORS_ALLOW_ALL_ORIGINS = True` 配置存在

### 3. 启动服务失败

**错误信息**：`Port 8000 is already in use`

**解决方法**：
- 使用其他端口启动：`python manage.py runserver 8001`
- 或者关闭占用 8000 端口的程序

### 4. Navicat 连接失败

**错误信息**：`Authentication failed`

**解决方法**：
- 在 Navicat 连接配置中取消勾选 "启用认证"
- 确保 MongoDB 没有启用密码认证

## 📚 学习资源

- Django 官方文档：https://docs.djangoproject.com/
- Django REST Framework 文档：https://www.django-rest-framework.org/
- MongoDB 官方文档：https://docs.mongodb.com/
- mongoengine 文档：https://docs.mongoengine.org/

## 🤝 贡献

如果您有任何问题或建议，欢迎随时交流！

---

**祝您学习愉快！** 🎉