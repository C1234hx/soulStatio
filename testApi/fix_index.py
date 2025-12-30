import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soulStation.settings')
django.setup()

from api.models import User
import mongoengine

# 连接已经在django.setup()中完成

# 直接操作集合来查看和删除索引
db = mongoengine.connection.get_db()
collection = db['users']

print("集合中的索引:")
indexes = collection.index_information()
for index_name, index_info in indexes.items():
    print(f"{index_name}: {index_info}")

# 删除email_1索引（如果存在）
if 'email_1' in indexes:
    print("\n删除email_1索引...")
    collection.drop_index('email_1')
    print("索引已删除")
    
    # 验证索引是否已删除
    print("\n更新后的索引:")
    updated_indexes = collection.index_information()
    for index_name, index_info in updated_indexes.items():
        print(f"{index_name}: {index_info}")
else:
    print("\nemail_1索引不存在")

# 测试创建一个新用户
print("\n测试创建新用户...")
try:
    user = User(
        username='testuser2',
        name='测试用户2',
        password='testpassword123',
        age=30,
        is_admin=False,
        is_active=True
    )
    user.save()
    print("用户创建成功!")
    print(f"用户ID: {user.id}")
    
    # 查询所有用户
    users = User.objects.all()
    print(f"\n当前用户数量: {users.count()}")
    for u in users:
        print(f"ID: {u.id}, 账号: {u.username}, 名称: {u.name}")
        
    # 删除测试用户
    user.delete()
    print("\n测试用户已删除")
except Exception as e:
    print(f"创建用户失败: {e}")