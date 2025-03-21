# Toy-RAG

## 项目简介
Toy-RAG 是一个基于向量检索的问答系统，旨在通过嵌入向量技术快速检索相关信息并生成回答。系统包含文档处理、向量化、向量存储和问答服务等模块。

## 系统架构
Toy-RAG 系统由以下几个核心模块组成：
1. 文档处理模块：负责原始文档的读取、分块和预处理
2. 向量化模块：将文本转换为向量表示
3. 向量存储模块：存储和检索向量数据
4. 问答服务模块：处理用户查询并生成回答

## 运行流程
1. 初始化阶段：
   - 读取原始文档
   - 对文档进行分块处理
   - 将文本块转换为向量
   - 将向量存储到向量数据库中
2. 问答阶段：
   - 接收用户查询
   - 将查询转换为向量
   - 在向量数据库中检索最相似的文档片段
   - 将检索结果传递给LLM生成最终回答

## 文件说明
- `main.py`: 程序入口，负责初始化系统和处理用户查询
- `document_processor.py`: 文档处理模块，负责文档的读取和分块
- `embedding_service.py`: 向量化模块，将文本转换为向量表示
- `vector_store.py`: 向量存储模块，负责向量的存储和检索
- `chat_service.py`: 问答服务模块，处理用户查询并生成回答
- `config.py`: 配置文件，存储API密钥等配置信息
- `path.py`: 路径管理模块，统一管理文件路径

## 安装说明
1. 克隆本仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 配置API密钥：在`config.py`中设置`ZHIPUAI_API_KEY`和`DEEPSEEK_API_KEY`
4. 初始化向量数据库：`python main.py --init`

## 使用方法
1. 将原始文档放入`database/rawFile`目录
2. 运行`python main.py`
3. 根据提示输入问题，系统将返回相关答案
4. 支持命令行参数：
   - `--init`: 初始化向量数据库
   - `--debug`: 开启调试模式

## 贡献指南
欢迎提交Pull Request。请确保代码风格一致，并添加适当的单元测试。
贡献前请阅读以下指南：
1. 使用PEP8代码风格
2. 为新增功能添加单元测试
3. 提交前确保所有测试通过
4. 使用描述性的commit message
