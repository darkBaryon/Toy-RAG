# Tiny RAG

一个轻量级的检索增强生成（RAG）实现，支持文档检索和问答功能。

## 功能特点

- 基于向量数据库的文档检索
- 使用 DeepSeek 进行智能问答
- 支持中文文档处理
- 灵活的文档嵌入和存储机制

## 项目结构

```
tiny_rag/
├── database/           # 存储向量数据和原始文件
├── llm.py             # DeepSeek聊天模型实现
├── main.py            # 主程序入口
├── path.py            # 路径处理工具
├── readFile.py        # 文件读取和处理
├── vectorBase.py      # 向量数据库实现
└── vectorization.py   # 文本向量化处理
```

## 环境配置

### 必需的环境变量
```bash
ZHIPU_API_KEY=your_zhipu_api_key      # 智谱AI的API密钥，用于文本向量化
DEEPSEEK_API_KEY=your_deepseek_api_key # DeepSeek的API密钥，用于问答生成
```

## 使用方法

1. 配置环境变量
2. 准备文档数据，放入 `database/rawFile` 目录
3. 运行程序：

```python
from main import main

# 设置参数
path = "database/rawFile"
query = "你的问题"

# 运行RAG
main(path=path, 
     embedding_api_key=zhipu_api_key, 
     chat_api_key=deepseek_api_key, 
     query=query)
```

## 工作流程

1. 文档处理：系统读取并处理输入文档
2. 向量化：使用智谱AI API将文档内容转换为向量
3. 相似度检索：根据用户问题检索最相关的文档片段
4. 问答生成：使用DeepSeek模型基于检索内容生成答案

## 注意事项

- 确保API密钥正确配置
- 文档存放位置需符合项目结构要求
- 检索结果默认返回top-5最相关片段
