import os
import json
from abc import ABC, abstractmethod
import ujson

from zhipuai import ZhipuAI
import numpy as np
import readFile


class EmbeddingBase(ABC):
    def __init__(self, chunk_list):
        """
        Initialize the EmbeddingBase class.

        Args:
            chunk_list (list): List of text chunks.
        """
        self.chunk_list = chunk_list
        self.embedded_vectors = []

    @abstractmethod
    def getVector(self):
        """
        Get the embedded vectors for the text chunks using an embedding tool.

        Returns:
            list: List of embedded vectors.
        """
        pass

    def saveVectors(self):
        
        """
        Save the embedded vectors to a file in the data/embeddedVector directory.
        """
        if not os.path.exists("data/embeddedVector"):
            os.makedirs("data/embeddedVector")
        with open("data/embeddedVector/embedded_vectors.json", "a") as f:
            json.dump(self.embedded_vectors, f)

class ZhiPuAIEembedding(EmbeddingBase):
    def __init__(self, api_key, chunk_list):
        """
        Initialize the ZhiPuAIEembedding class.

        Args:
            api_key (str): ZhiPuAI API key.
            chunk_list (list): List of text chunks.
        """
        super().__init__(chunk_list)
        self.api_key = api_key

    def getVector(self, model: str = "embedding-3", input_size: int = 64):
        """
        Calculate the embedding vector for a given text using ZhiPUAI's API.
        
        Args:
            text (str): The input text to embed
            model (str): The ZhiPuAI model to use for embedding. Defaults to "embedding-3"
        
        Returns:
            List[float]: The embedding vector
        
        Note:
            Requires ZhiPuAI_API_KEY environment variable to be set
        """
        client = ZhipuAI(api_key=self.api_key)

        for i in range(0, len(self.chunk_list)//input_size + 1):
            if i == len(self.chunk_list)//input_size:
                text = self.chunk_list[i*input_size:]
            else:
                text = self.chunk_list[i*input_size:(i+1)*input_size]
        
            # Get the embedding from OpenAI
            response = client.embeddings.create(
                model=model,
                input=text,
                encoding_format="float"
            )
            
            self.embedded_vectors.extend([data.embedding[:] for data in response.data])
        
        # Return the embedding vector
        return self.chunk_list, self.embedded_vectors
    
    
if __name__ == "__main__":
    
    path = os.path.join(os.path.dirname(__file__), 'database/rawFile/Git Tutorial_1.md')
    
    # Read and split the text content of a dictionary into chunks of size not exceeding 128.
    chunk_list = readFile.ReadFile(path=path, query=None).split_text_into_chunks()[:2]

    #chunk_list = ["Hello, how are you?", "I am doing great today!", "What are you up to?"]
    api_key = "3d5e610d6c3748d994b940cd038cf3f7.zWNI1CDqf92JSwdv"

    chunk_list, embedded_vectors = ZhiPuAIEembedding(api_key, chunk_list).getVector()
    print('chunk_list:', chunk_list)
    print('embedded_vectors:', embedded_vectors[0][:2])

    """
    Save the embedded vectors to a file in the data/embeddedVector directory.
    """
    if not os.path.exists("database/embeddedVector"):
        os.makedirs("database/embeddedVector")
    with open("database/embeddedVector/embedded_vectors.json", "w") as f:
        data = [[chunk_list[i], embedded_vectors[i][:3]] for i in range(len(chunk_list))]
        json.dump(data, f)
    print("Saved as database/embeddedVector/embedded_vectors.json.")

    with open("database/embeddedVector/embedded_vectors.json", "r") as f:
        datas = f.read()
        data = ujson.loads(datas)
    print('embedded_vectors:', data[0][1])
    print('chunk:', data[0][0])
    #print('embedded_vectors:', data[1][1])
    #print('chunk:', data[1][0])