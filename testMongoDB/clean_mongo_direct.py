import os
import django
from pymongo import MongoClient

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soulStation.settings')
django.setup()

from django.conf import settings

# 获取MongoDB配置
mongo_settings = settings.MONGODB_SETTINGS

# 直接连接MongoDB
client = MongoClient(
    host=mongo_settings['host'],
    port=mongo_settings['port'],
    username=mongo_settings['username'],
    password=mongo_settings['password'],
    authSource='admin'
)

db = client[mongo_settings['db']]
collection = db['users']

print("清理MongoDB中的users集合...")

# 删除整个集合（包含数据和索引）
collection.drop()

print("集合已删除")

# 重新创建集合
collection = db['users']

# 添加username唯一索引
collection.create_index([('username', 1)], unique=True)

print("集合已重新创建，并添加了username唯一索引")

# 测试插入新用户
new_user = {
    'username': 'admin',
    'name': '管理员',
    'password': 'admin123',
    'age': 30,
    'is_admin': True,
    'is_active': True,
    'created_at': '2025-12-26T10:00:00',
    'updated_at': '2025-12-26T10:00:00'
}

result = collection.insert_one(new_user)
print(f"已创建管理员用户，ID: {result.inserted_id}")

# 查看集合中的索引
print("\n集合索引:")
indexes = collection.index_information()
for index_name, index_info in indexes.items():
    print(f"{index_name}: {index_info}")

# 关闭连接
client.close()
print("\n清理完成!")