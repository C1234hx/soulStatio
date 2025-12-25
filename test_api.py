import requests
import json

# 测试URL
BASE_URL = 'http://127.0.0.1:8000/api/'

print("测试Django REST API与MongoDB连接...")

# 测试1: 获取所有用户
print("\n1. 测试获取所有用户:")
try:
    response = requests.get(BASE_URL + 'users/')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"错误: {e}")

# 测试2: 创建新用户
print("\n2. 测试创建新用户:")
try:
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'age': 25
    }
    response = requests.post(BASE_URL + 'users/', data=json.dumps(user_data), 
                          headers={'Content-Type': 'application/json'})
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    # 保存创建的用户ID用于后续测试
    if response.status_code == 201:
        user_id = response.json().get('id')
        print(f"创建的用户ID: {user_id}")
except Exception as e:
    print(f"错误: {e}")
    user_id = None

# 测试3: 获取单个用户
print("\n3. 测试获取单个用户:")
if user_id:
    try:
        response = requests.get(BASE_URL + f'users/{user_id}/')
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
    except Exception as e:
        print(f"错误: {e}")

# 测试4: 更新用户信息
print("\n4. 测试更新用户信息:")
if user_id:
    try:
        update_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'age': 30
        }
        response = requests.put(BASE_URL + f'users/{user_id}/', data=json.dumps(update_data), 
                              headers={'Content-Type': 'application/json'})
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
    except Exception as e:
        print(f"错误: {e}")

# 测试5: 再次获取所有用户
print("\n5. 测试再次获取所有用户:")
try:
    response = requests.get(BASE_URL + 'users/')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"错误: {e}")

print("\n测试完成!")
