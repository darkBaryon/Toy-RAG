from vector_store import VectorBase
from chat_service import DeepSeekChat
from config import Config
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(embedding_api_key, chat_api_key, query, path='./database/embeddedVector/'):
    try:
        vectorbase = VectorBase()
        
        # 添加向量到数据库
        try:
            vectorbase.addVector(path=path, api_key=embedding_api_key)
            logging.info(f"Successfully added vectors from {path}")
        except Exception as e:
            logging.error(f"Error adding vectors: {str(e)}")
            return
        
        # 查询相似文本块
        top_k = 5
        try:
            similar_chunks = vectorbase.queryVectors(query=query, top_k=top_k, file_path=path)
            if not similar_chunks:
                logging.warning("No similar chunks found")
                return
            
            logging.info(f"Found {len(similar_chunks)} similar chunks")
            for chunk in similar_chunks:
                print(chunk)
                print('*'*150)
        except Exception as e:
            logging.error(f"Error querying vectors: {str(e)}")
            return

        # 构建消息并调用LLM
        message = {
            "role": "user",
            "content": f"Question:{query}?,\
                    问题背景:{similar_chunks};\
                    根据提供的问题背景，回答问题;\
                    如果背景中没有相关内容, 回复\"答案不存在\", 并返回全部背景内容."
        }
        try:
            deepseek = DeepSeekChat(chat_api_key=chat_api_key).chat(messages=[message])
            print(deepseek)
            logging.info("Successfully generated response")
        except Exception as e:
            logging.error(f"Error calling LLM: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    # 参数配置
    path = "database/rawFile"
    zhipu_api_key = Config.ZHIPUAI_API_KEY
    deepseek_api_key = Config.DEEPSEEK_API_KEY
    
    if not deepseek_api_key:
        logging.error("DEEPSEEK_API_KEY not set in config")
        exit(1)
    
    # 待回答的问题
    query = "上海交通大学出差报销特聘教授住宿标准是多少?"
    
    # 运行主程序
    main(path=path, embedding_api_key=zhipu_api_key, chat_api_key=deepseek_api_key, query=query)