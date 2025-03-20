import os
import sys
import json
from typing import List, Dict, Any
from document_processor import ReadFile
from embedding_service import ZhiPuAIEmbedding
from config import Config
from path import find_generated_path


class VectorBase:
    MODEL = Config.ZHIPUAI_MODEL
    API_KEY = Config.ZHIPUAI_API_KEY
    
    """Vector database management class responsible for vector storage, retrieval and management.
    
    Main functions:
    - Calculate vector representations of text
    - Store vectors to file system
    - Load stored vectors
    - Process vectorization of single files and folders
    
    Attributes:
        vector_storage_dir (str): Vector storage directory
        raw_file_dir (str): Raw file directory
    """
    
    def __init__(self):
        """Initialize vector database management class."""
        self.vector_storage_dir = Config.VECTOR_STORAGE_DIR
        self.raw_file_dir = Config.RAW_FILE_DIR

    def calculate_vector(self, filepath: str = None, query: str = None) -> List[List[Any]]:
        """Calculate vector representation of text.

        Args:
            filepath: File path
            query: Query text

        Returns:
            List[List[Any]]: List containing text chunks and corresponding vectors

        Raises:
            Exception: If text processing or vector calculation fails
        """
        try:
            if filepath:
                chunk_list = ReadFile(path=filepath).split_text_into_chunks()
            elif query:
                chunk_list = ReadFile(query=query).split_text_into_chunks()
            else:
                raise ValueError("Either filepath or query must be provided")

            chunk_list, embedded_vectors = ZhiPuAIEmbedding(chunk_list).get_vectors()
            return [[chunk_list[i], embedded_vectors[i]] for i in range(len(chunk_list))]
        except Exception as e:
            raise Exception(f"Error calculating vectors: {str(e)}")

    def save_vectors(self, filepath: str, embedded_vectors_array: List[List[Any]]) -> str:
        """Save vectors to the file system.

        Args:
            filepath: Path to the original file
            embedded_vectors_array: Vector data

        Returns:
            str: Path to the saved file

        Raises:
            Exception: If there's an error during the save process
        """
        try:
            generate_path = find_generated_path(filepath)
            folder_path = os.path.dirname(generate_path)
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                
            with open(generate_path, 'w') as f:
                json.dump(embedded_vectors_array, f)
                
            return generate_path
        except Exception as e:
            raise Exception(Config.ERROR_MESSAGES["file_save_error"].format(str(e)))
        
    def addVector_single_file(self, filepath: str):
        
        # 计算嵌入向量
        embedded_vectors_array = self.calculate_vector(filepath)
        self.save_vectors(filepath=filepath, embedded_vectors_array=embedded_vectors_array)
        
        return embedded_vectors_array     
       
    def addVector(self, path: str, api_key: str, model: str = MODEL):
        
        # Check if the path exists
        if not os.path.exists(path):
            print(f"{path} not exists.")
            sys.exit(1)
        if api_key != Config.ZHIPUAI_API_KEY:
            print(f"Wrong API_KEY.")
            sys.exit(2)
        if model != Config.ZHIPUAI_MODEL:
            print(f"Wrong model.")
            sys.exit(3)
        
        # 如果输入为文件夹路径, 遍历文件
        if os.path.isdir(path):
            """Read and return the text_dict of all files in a folder."""
            folder_path = path
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        self.addVector_single_file(filepath=file_path)
                        
        # 如果输入为文件路径, 把本文件的vector加入到embedded_vectors.json文件中
        ## 用于数据库增加数据, 避免增加数据时对原有数据重新计算vector
        if os.path.isfile(path):
            filepath = path
            with open(path, 'r', encoding='utf-8') as file:
                self.addVector_single_file(filepath=filepath)
                    
    def deleteVector(self, raw_file_path):
        
        # Check if the path exists
        if not os.path.exists(raw_file_path):
            print(f"{raw_file_path} not exists.")
            sys.exit(1)
        
        generated_file_path = find_generated_path(raw_file_path)
        
        if os.path.isfile(generated_file_path):
            # If it's a file, delete the corresponding generated file
            if os.path.exists(generated_file_path):
                os.remove(generated_file_path)
                print(f"Deleted {generated_file_path}")
        elif os.path.isdir(generated_file_path):
            if os.path.exists(generated_file_path):
                shutil.rmtree(generated_file_path)
            print(f"Deleted {generated_file_path}")

    def loadVectors(self, raw_file_path: str):
        
        # Check if the path exists
        if not os.path.exists(raw_file_path):
            print(f"{raw_file_path} not exists.")
            sys.exit(1)
            
        generated_file_path = find_generated_path(raw_file_path)
        if os.path.isfile(generated_file_path):
            if os.path.exists(generated_file_path):
                with open(generated_file_path, 'r') as f:
                    vector_array = json.load(f)
                    print(f"Loaded {generated_file_path}")
                    return vector_array
            else:
                print(f"{generated_file_path} not exists.")
                
        else:
            vector_list = []
            
            if not os.path.exists(generated_file_path):
                print(f"{generated_file_path} not exists.")
                
            for root, dirs, files in os.walk(generated_file_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = f.read()
                        vector_array = json.loads(data)
                        vector_list.extend(vector_array)
                    print(f"Loaded {file_path}")
            return vector_list

    def queryVectors(self, query: str, top_k: int = 10, file_path: str = "database/embeddedVector/"):
        # 使用嵌入向量计算相似度
        import numpy as np
        query_vector = self.calculate_vector(query=query)
        loadedVectors = self.loadVectors(file_path)
        
        if not loadedVectors or not query_vector:
            return []
            
        # 计算余弦相似度
        similarities = []
        query_vec = np.array(query_vector[0][1])
        query_norm = np.linalg.norm(query_vec)
        
        for vector in loadedVectors:
            vec = np.array(vector[1])
            vec_norm = np.linalg.norm(vec)
            if query_norm == 0 or vec_norm == 0:
                similarities.append(0)
            else:
                similarity = np.dot(query_vec, vec) / (query_norm * vec_norm)
                similarities.append(similarity)
                
        # 获取top-k结果
        top_k_indices = np.argsort(similarities)[-top_k:][::-1]  # 反转以获得降序排列
        return [loadedVectors[i][0] for i in top_k_indices]

    def append_to_file(self, file_path: str, content: str):
        with open(file_path, 'a') as f:
            f.write(content + '\n')
            


if __name__ == '__main__': 
    
    path = "database/rawFile/差旅费管理"
    api_key = "3d5e610d6c3748d994b940cd038cf3f7.zWNI1CDqf92JSwdv"
    model = "embedding-3"
    
    vectorBase = vectorBase()
    
    vectorBase.addVector(path=path, api_key=api_key, model=model)
    
    #vector_loaded = vectorBase.loadVectors(raw_file_path="database/embeddedVector/Git Tutorial_1.json")
    
    #vectorBase.deleteVector(raw_file_path=path)
    
    query = "上海交通大学出差报销特聘教授住宿标准是多少?"
    top_k = 5
    similar_chunks = vectorBase.queryVectors(query=query, top_k=top_k, file_path=path)
    for chunk in similar_chunks:
        print(chunk)
        print('*'*100)
    
    from openai import OpenAI
    message = {
        "role": "user",
        "content": f"Question:{query}?,\
                问题背景:{similar_chunks};\
                根据提供的问题背景，回答问题;\
                如果背景中没有相关内容, 回复“答案不存在”, 并返回全部背景内容."
    }
    message = [message]
    deepseek_api_key = 'sk-3c391edfe572451a843b0a2ddbac9050'
    client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
            model="deepseek-chat",
            messages=message
        )
    print(response.choices[0].message)