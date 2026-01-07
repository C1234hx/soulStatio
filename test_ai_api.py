import requests
import json

# 测试心理咨询聊天API的POST接口
def test_psychological_chat_post():
    # API端点
    url = "http://127.0.0.1:8000/api/psychological-chat/"
    
    # 测试数据
    test_data = {
        "content": "我最近工作压力很大，该怎么办？"
    }
    
    print("正在测试心理咨询聊天API的POST接口...")
    try:
        # 发送POST请求
        response = requests.post(url, json=test_data)
        
        # 打印响应状态码
        print(f"响应状态码: {response.status_code}")
        
        # 打印响应内容
        response_data = response.json()
        print("响应内容:")
        print(json.dumps(response_data, ensure_ascii=False, indent=2))
        
        # 检查是否成功
        if response.status_code == 200:
            print("测试成功！API正常工作。")
            
            # 检查是否包含用户消息和AI消息
            if "user_message" in response_data["data"] and "ai_message" in response_data["data"]:
                print("\n用户消息:")
                print(json.dumps(response_data["data"]["user_message"], ensure_ascii=False, indent=2))
                print("\nAI消息:")
                print(json.dumps(response_data["data"]["ai_message"], ensure_ascii=False, indent=2))
        else:
            print("测试失败！API返回错误状态码。")
            
    except Exception as e:
        print(f"测试失败！发生异常: {str(e)}")

# 测试AI接口直接调用
def test_ai_direct_call():
    url = "https://spark-api-open.xf-yun.com/v2/chat/completions"
    api_key = "Bearer tRZtbLSChHuywNRdCHwk:xnetczCFiBixgYvFOdWL"
    
    data = {
        "max_tokens": 1000,
        "top_k": 6,
        "temperature": 1.2,
        "messages": [
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": "我最近工作压力很大，该怎么办？"
            }
        ],
        "model": "x1",
        "tools": [
            {
                "web_search": {
                    "search_mode": "normal",
                    "enable": True
                },
                "type": "web_search"
            }
        ]
    }
    
    data["stream"] = True
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    
    print("\n正在测试AI接口直接调用...")
    try:
        response = requests.post(url, json=data, headers=headers, stream=True)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code != 200:
            print(f"AI接口错误: {response.text}")
            return
        
        # 处理流式响应
        ai_content = ""
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                print(f"原始行: {line_str}")
                if line_str.startswith('data: '):
                    line_str = line_str[6:]
                
                if line_str:
                    try:
                        line_data = json.loads(line_str)
                        if line_data.get("choices", [{}])[0].get("finish_reason") == "stop":
                            break
                        delta_content = line_data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        if delta_content:
                            ai_content += delta_content
                            print(f"AI回复: {delta_content}")
                    except json.JSONDecodeError as e:
                        print(f"JSON解析错误: {e}")
        
        print(f"\n完整AI回复: {ai_content}")
        
    except Exception as e:
        print(f"测试失败！发生异常: {str(e)}")

if __name__ == "__main__":
    # 测试心理咨询聊天API
    test_psychological_chat_post()
    
    # 测试AI接口直接调用
    test_ai_direct_call()  # 启用直接调用AI接口的测试