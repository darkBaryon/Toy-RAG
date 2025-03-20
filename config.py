# Configuration settings for the RAG system

class Config:
    # ZhiPuAI API settings
    ZHIPUAI_API_KEY = "3d5e610d6c3748d994b940cd038cf3f7.zWNI1CDqf92JSwdv"
    DEEPSEEK_API_KEY = "sk-3c391edfe572451a843b0a2ddbac9050"
    ZHIPUAI_MODEL = "embedding-3"
    
    # Text chunking settings
    CHUNK_SIZE = 128
    CHUNK_OVERLAP = 20
    
    # Vector storage settings
    VECTOR_STORAGE_DIR = "database/embeddedVector"
    RAW_FILE_DIR = "database/rawFile"
    
    # Batch processing settings
    EMBEDDING_BATCH_SIZE = 64
    
    # Error messages
    ERROR_MESSAGES = {
        "path_not_exist": "Path does not exist: {}",
        "invalid_api_key": "Invalid API key provided",
        "invalid_model": "Invalid model specified",
        "file_save_error": "Error saving file: {}"
    }