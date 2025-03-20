from vectorBase import vectorBase
from llm import DeepSeekChat
import os


def main(embedding_api_key, chat_api_key,query, path = './database/embeddedVector/'):
    
    vectorbase = vectorBase()
    
    vectorbase.addVector(path=path, api_key=embedding_api_key)
    
    top_k = 5
    similar_chunks = vectorbase.queryVectors(query=query, top_k=top_k, file_path=path)
    for chunk in similar_chunks:
        print(chunk)
        print('*'*150)

    message = {
        "role": "user",
        "content": f"Question:{query}?,\
                问题背景:{similar_chunks};\
                根据提供的问题背景，回答问题;\
                如果背景中没有相关内容, 回复“答案不存在”, 并返回全部背景内容."
    }
    message = [message]
    deepseek = DeepSeekChat(chat_api_key=deepseek_api_key).chat(messages=message)
    print(deepseek)



if __name__ == '__main__':
    
    # parameters
    path = "database/rawFile"
    zhipu_api_key = os.getenv('ZHIPU_API_KEY')
    deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
    
    
    # question to be answered
    query = "上海交通大学出差报销特聘教授住宿标准是多少?"
    
    # run
    main(path=path, embedding_api_key=zhipu_api_key, chat_api_key=deepseek_api_key, query=query)