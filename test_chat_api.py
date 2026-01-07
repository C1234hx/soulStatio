import requests
import json
import time

# 测试心理咨询聊天API
def test_psychological_chat():
    url = 'http://127.0.0.1:8000/api/psychological-chat/'
    
    # 测试数据
    test_data = {
        'content': '你好，我今天心情不太好'
    }
    
    print('正在调用心理咨询聊天API...')
    start_time = time.time()
    
    try:
        # 设置超时时间为150秒，确保超过后端的120秒设置
        response = requests.post(url, json=test_data, timeout=150)
        end_time = time.time()
        
        print(f'调用耗时: {end_time - start_time:.2f} 秒')
        print(f'状态码: {response.status_code}')
        print(f'响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}')
        
        return response.json()
    except requests.exceptions.Timeout:
        end_time = time.time()
        print(f'调用超时! 耗时: {end_time - start_time:.2f} 秒')
        return {'error': 'timeout'}
    except Exception as e:
        end_time = time.time()
        print(f'调用失败! 耗时: {end_time - start_time:.2f} 秒, 错误: {str(e)}')
        return {'error': str(e)}

if __name__ == '__main__':
    test_psychological_chat()