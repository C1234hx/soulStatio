import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soulStation.settings')
django.setup()

from api.models import User

print("数据库中现有的用户:")
users = User.objects.all()
print(f"用户总数: {users.count()}")
for user in users:
    print(f"ID: {user.id}, 账号: {user.username}, 名称: {user.name}, 管理员: {user.is_admin}, 状态: {user.is_active}")

# 删除测试用户
print("\n删除测试用户...")
test_users = User.objects.filter(username__in=['testuser', 'testuser2', 'updateduser'])
deleted_count = test_users.delete()
print(f"已删除 {deleted_count} 个测试用户")

# 查看剩余用户
print("\n剩余用户:")
remaining_users = User.objects.all()
print(f"用户总数: {remaining_users.count()}")
for user in remaining_users:
    print(f"ID: {user.id}, 账号: {user.username}, 名称: {user.name}, 管理员: {user.is_admin}, 状态: {user.is_active}")
