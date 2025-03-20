from vector_store import VectorBase
from chat_service import DeepSeekChat
from config import Config
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def query(query):
    try:
        vectorbase = VectorBase()
        path = 'database/embeddedVector/差旅费管理/'
        
        # 查询相似文本块
        top_k = 5
        similar_chunks = vectorbase.queryVectors(query=query, top_k=top_k, file_path=path)
        if not similar_chunks:
            logging.warning("No similar chunks found")
            return
        
        logging.info(f"Found {len(similar_chunks)} similar chunks")
        
        # 构建消息并调用LLM
        message = {
            "role": "user",
            "content": f"Question:{query}?,\
                    问题背景:{similar_chunks};\
                    根据提供的问题背景，回答问题;\
                    如果背景中没有相关内容, 回复\"答案不存在\", 并返回全部背景内容."
        }
        deepseek = DeepSeekChat(chat_api_key=Config.DEEPSEEK_API_KEY).chat(messages=[message])
        return deepseek
        logging.info("Successfully generated response")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    # 待回答的问题
    query_str = "上海交通大学出差报销特聘教授住宿标准是多少?"
    query(query_str)