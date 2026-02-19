md5_path = "./md5.txt"

#Chroma
collection_name = "rag"
persist_directory = "./chroma_db"

#splitter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", ",", "，", "。", "！", "？"] #文本分割的分隔符列表
max_spliter_char_number = 1000 #文本分割的最大字符数，没超过这个数就不分割了

#
similarity_threshold = 2 #检索返回匹配的文档数量

embedding_model_name = "text-embedding-v4" #嵌入模型名称
chat_model_name = "qwen3-max" #聊天模型名称

#session_id配置
session_config = {
    "configurable":{
        "session_id": "user_002"
    }
}