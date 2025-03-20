# api.py

from openai import OpenAI, chat


class AIChat:
    def __init__(self, chat_api_key):
        self.chat_api_key = chat_api_key

    def chat(self, message):
        raise NotImplementedError("必须实现 chat 方法")

class DeepSeekChat(AIChat):
    def __init__(self, chat_api_key):
        super().__init__(chat_api_key)

    def chat(self, messages):
        client = OpenAI(api_key=self.chat_api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        return response.choices[0].message

# 使用示例
if __name__ == "__main__":
    
    
    api = 'sk-3c391edfe572451a843b0a2ddbac9050'
    chat = DeepSeekChat(api)
    response = chat.chat(message="如何安装git")
    print(response)