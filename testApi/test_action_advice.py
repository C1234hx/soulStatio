import requests
import json

# 测试URL
BASE_URL = 'http://127.0.0.1:8000/api/'

print("测试行动建议API...")
print("=" * 50)

# 测试1: 获取所有行动建议
print("\n1. 测试获取所有行动建议:")
try:
    response = requests.get(BASE_URL + 'action-advice/')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"错误: {e}")

# 测试2: 创建新的行动建议
print("\n2. 测试创建新的行动建议:")
try:
    advice_data = {
        'emotion_direction': 0,
        'content': '当你感到开心时，可以尝试记录下这些美好时刻，这会让你的幸福感更持久。',
        'is_active': True
    }
    response = requests.post(BASE_URL + 'action-advice/', data=json.dumps(advice_data), 
                          headers={'Content-Type': 'application/json'})
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    # 保存创建的行动建议ID用于后续测试
    if response.status_code == 201:
        advice_id = response.json().get('id')
        print(f"创建的行动建议ID: {advice_id}")
    else:
        advice_id = None
except Exception as e:
    print(f"错误: {e}")
    advice_id = None

# 测试3: 创建另一个不同情绪向的行动建议
print("\n3. 测试创建负面情绪的行动建议:")
try:
    advice_data_negative = {
        'emotion_direction': 2,
        'content': '当你感到焦虑时，可以尝试深呼吸练习，每次吸气4秒，屏息4秒，呼气6秒，重复5次。',
        'is_active': True
    }
    response = requests.post(BASE_URL + 'action-advice/', data=json.dumps(advice_data_negative), 
                          headers={'Content-Type': 'application/json'})
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"错误: {e}")

# 测试4: 获取单个行动建议
print("\n4. 测试获取单个行动建议:")
if advice_id:
    try:
        response = requests.get(BASE_URL + f'action-advice/{advice_id}/')
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
    except Exception as e:
        print(f"错误: {e}")

# 测试5: 更新行动建议
print("\n5. 测试更新行动建议:")
if advice_id:
    try:
        update_data = {
            'emotion_direction': 0,
            'content': '当你感到开心时，可以尝试记录下这些美好时刻，分享给朋友，这会让你的幸福感更持久。',
            'is_active': False
        }
        response = requests.put(BASE_URL + f'action-advice/{advice_id}/', data=json.dumps(update_data), 
                              headers={'Content-Type': 'application/json'})
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
    except Exception as e:
        print(f"错误: {e}")

# 测试6: 再次获取所有行动建议
print("\n6. 测试再次获取所有行动建议:")
try:
    response = requests.get(BASE_URL + 'action-advice/')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"错误: {e}")

# 测试7: 删除行动建议
print("\n7. 测试删除行动建议:")
if advice_id:
    try:
        response = requests.delete(BASE_URL + f'action-advice/{advice_id}/')
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text if response.text else '删除成功，无返回内容'}")
    except Exception as e:
        print(f"错误: {e}")

# 测试8: 验证删除结果
print("\n8. 验证删除结果:")
try:
    response = requests.get(BASE_URL + 'action-advice/')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 50)
print("测试完成!")