import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api/users/'

print("直接测试API接口...")

# 测试获取所有用户
print("\n1. 测试GET /api/users/")
try:
    response = requests.get(BASE_URL)
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"响应内容: {response.text[:500]}...")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

# 测试创建用户
print("\n2. 测试POST /api/users/")
try:
    user_data = {
        'username': 'direct_test',
        'name': '直接测试用户',
        'password': 'test123',
        'age': 28,
        'is_admin': False,
        'is_active': True
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(BASE_URL, data=json.dumps(user_data), headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    print(f"响应内容: {response.text}")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成!")
