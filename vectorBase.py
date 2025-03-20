import os
import sys
import json
import shutil
import ujson
from readFile import ReadFile
from vectorization import ZhiPuAIEembedding
from path import find_generated_path


class vectorBase():
    
    '''
    def __init__(self):
    Initialize the vectorBase class
    
    def getVector(self, model: str = "embedding-3"):
    Calculate the embedding vector for a given text using ZhiPUAI's API.
    
    def saveVectors(self):
    Save the embedded vectors to a file in the data/embeddedVector directory.
    
    def loadVectors(self, file_path: str):
    Load the embedded vectors from a file in the data/embeddedVector directory.
    
    def queryVectors(self, query: str):
    Query the embedded vectors for the most similar vector to the input query.
    
    '''
    
    API_KEY = "3d5e610d6c3748d994b940cd038cf3f7.zWNI1CDqf92JSwdv"
    MODEL = "embedding-3"
    
    def __init__(self):
        
        self.api_key = self.API_KEY
        self.model = self.MODEL

    def calculate_vector(self, filepath: str = None, query: str = None):
        # ReadFile类的split_text_into_chunks方法
        # 使用 ZhiPUAI 的 API 计算嵌入向量
        # 调用vectorization.py中的ZhiPuAIEembedding类
        # 传入API key和chunk list
        # 返回计算得到的嵌入向量
        if filepath != None:
            chunk_list = ReadFile(path=filepath).split_text_into_chunks()
        elif query != None:
            chunk_list = ReadFile(query=query).split_text_into_chunks()
        chunk_list, embedded_vectors= ZhiPuAIEembedding(api_key=self.api_key, chunk_list=chunk_list).getVector(self.model) 
        embedded_vectors_array = [[chunk_list[i], embedded_vectors[i][:]] for i in range(len(chunk_list))]
        return embedded_vectors_array

    def saveVectors(self, filepath: str, embedded_vectors_array):
        
        # 保存嵌入向量到文件
        generate_path = find_generated_path(filepath)
        
        folder_path = os.path.dirname(generate_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(generate_path, 'w') as f:
            json.dump(embedded_vectors_array, f)
        print(f"Saved in {generate_path}.")
        
    def addVector_single_file(self, filepath: str):
        
        # 计算嵌入向量
        embedded_vectors_array = self.calculate_vector(filepath)
        self.saveVectors(filepath=filepath, embedded_vectors_array=embedded_vectors_array)
        
        return embedded_vectors_array     
       
    def addVector(self, path: str, api_key: str, model: str = MODEL):
        
        # Check if the path exists
        if not os.path.exists(path):
            print(f"{path} not exists.")
            sys.exit(1)
        if api_key != self.API_KEY:
            print(f"Wrong API_KEY.")
            sys.exit(2)
        if model != self.MODEL:
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
        if not os.path.exists(path):
            print(f"{path} not exists.")
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
                    vector_array = ujson.load(f)
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
                        vector_array = ujson.loads(data)
                        vector_list.extend(vector_array)
                    print(f"Loaded {file_path}")
            return vector_list

    def queryVectors(self, query: str, top_k: int = 10, file_path: str = "database/embeddedVector/"):
        # 使用嵌入向量计算相似度
        # 这里需要实现具体的相似度计算逻辑
        # 例如使用余弦相似度
        import numpy as np
        query_vector = self.calculate_vector(query = query)
        loadedVectors = self.loadVectors(file_path)
        
        similarities = []
        for vector in loadedVectors:
            similarity = np.dot(query_vector[0][1], vector[1]) / (np.linalg.norm(query_vector[0][1]) * np.linalg.norm(vector[1]))
            similarities.append(similarity)
        top_k_indices = np.argsort(similarities)[-top_k:]
        print(top_k_indices)
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