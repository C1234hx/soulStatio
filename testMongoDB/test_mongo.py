import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soulStation.settings')
django.setup()

# 测试MongoDB连接
from api.models import User

print("测试MongoDB连接...")

# 尝试获取所有用户
try:
    users = User.objects.all()
    print(f"成功连接到MongoDB，当前有 {users.count()} 个用户")
except Exception as e:
    print(f"MongoDB连接失败: {e}")
    import traceback
    traceback.print_exc()

# 尝试创建一个用户
try:
    print("\n尝试创建一个测试用户...")
    user = User(
        username='test_mongo',
        name='测试Mongo用户',
        password='test123',
        age=30,
        is_admin=False,
        is_active=True
    )
    user.save()
    print(f"成功创建用户，ID: {user.id}")
    
    # 尝试查询用户
    user_from_db = User.objects.get(id=user.id)
    print(f"成功查询用户: {user_from_db.name}")
    
    # 尝试删除用户
    user_from_db.delete()
    print("成功删除用户")
except Exception as e:
    print(f"数据库操作失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成!")
