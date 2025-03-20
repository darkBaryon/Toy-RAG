from abc import ABC, abstractmethod
from zhipuai import ZhipuAI
from config import Config
from typing import List, Tuple


class EmbeddingBase(ABC):
    def __init__(self, chunk_list: List[str]):
        """
        Initialize the EmbeddingBase class.

        Args:
            chunk_list (List[str]): List of text chunks to be embedded.
        """
        self.chunk_list = chunk_list
        self.embedded_vectors = []

    @abstractmethod
    def get_vectors(self) -> Tuple[List[str], List[List[float]]]:
        """
        Get the embedded vectors for the text chunks using an embedding tool.

        Returns:
            Tuple[List[str], List[List[float]]]: A tuple containing the original chunks and their embeddings.
        """
        pass

class ZhiPuAIEmbedding(EmbeddingBase):
    def __init__(self, chunk_list: List[str]):
        """
        Initialize the ZhiPuAIEmbedding class.

        Args:
            chunk_list (List[str]): List of text chunks to be embedded.
        """
        super().__init__(chunk_list)
        self.api_key = Config.ZHIPUAI_API_KEY

    def get_vectors(self) -> Tuple[List[str], List[List[float]]]:
        """
        Calculate the embedding vectors for the text chunks using ZhiPuAI's API.
        
        Returns:
            Tuple[List[str], List[List[float]]]: A tuple containing the original chunks and their embeddings.
        
        Raises:
            Exception: If there's an error during the embedding process.
        """
        try:
            client = ZhipuAI(api_key=self.api_key)
            batch_size = Config.EMBEDDING_BATCH_SIZE

            for i in range(0, len(self.chunk_list) // batch_size + 1):
                if i == len(self.chunk_list) // batch_size:
                    batch = self.chunk_list[i * batch_size:]
                else:
                    batch = self.chunk_list[i * batch_size:(i + 1) * batch_size]
                
                if not batch:
                    continue

                response = client.embeddings.create(
                    model=Config.ZHIPUAI_MODEL,
                    input=batch,
                    encoding_format="float"
                )
                
                self.embedded_vectors.extend([data.embedding[:] for data in response.data])
            
            return self.chunk_list, self.embedded_vectors
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")
    
    
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