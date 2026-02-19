"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str: str):
    """
    检查传入的MD5值是否已经被处理过了
    return false if 没有处理过，true if 处理过了
    """
    if not os.path.exists(config.md5_path):
        #文件不存在，说明没有处理过任何文件，直接返回False
        open(config.md5_path, "w", encoding='utf-8').close() #创建一个空的md5.txt文件
        return False
    else:
        for line in open(config.md5_path, "r", encoding='utf-8').readlines():
            line = line.strip() #去掉行末的空格和回车
            if line == md5_str:
                return True
        return False
    
def save_md5(md5_str: str):
    """
    将新的MD5值保存到文件中
    """
    open(config.md5_path, "a", encoding='utf-8').write(md5_str + "\n") #追加写入文件

def get_string_md5(md5_str: str, encoding="utf-8"):
    """
    获取字符串的MD5值
    """
    #将字符串转换为bytes字节数组
    str_bytes = md5_str.encode(encoding=encoding)
    
    #创建MD5对象
    md5_obj = hashlib.md5() #得到md5对象
    md5_obj.update(str_bytes) #更新MD5对象的内容
    md5_hex = md5_obj.hexdigest() #得到MD5值的十六进制字符串表示

    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        #如果数据库文件存储路径不存在，则创建
        os.makedirs(config.persist_directory, exist_ok=True) #创建数据库文件存储路径
        
        self.chroma = Chroma(
            collection_name=config.collection_name,#数据库表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory #数据库文件存储路径
            ) #向量存储的实例Chroma向量库对象
        
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, #每个文本块的最大长度
            chunk_overlap=config.chunk_overlap, #文本块之间的重叠长度
            separators=config.separators, #文本分割的分隔符列表
            length_function=len #计算文本长度的函数 python自带的len工具
            ) #文本分割器实例
    
    def upload_by_str(self, data: str, filename):
        """
        通过字符串上传数据到知识库
        """
        #1.计算字符串的MD5值
        md5_str = get_string_md5(data)
        
        #2.检查MD5值是否已经处理过了
        if check_md5(md5_str):
            return f"文件 {filename} 已经存在知识库中，跳过上传"
        
        #3.如果没有处理过，则进行文本分割和向量化，并保存到数据库中
        if len(data) > config.max_spliter_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data) #文本分割器实例的split_text方法进行文本分割，得到一个文本块列表
        else:
            knowledge_chunks = [data]
        
        
        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "syy"
        }
        self.chroma.add_texts(
            #iterable -> list \ tuple
            knowledge_chunks, #文本块列表
            metadatas=[metadata for _ in knowledge_chunks],
            ) #将文本块列表添加到Chroma向量库中，同时添加元数据（文件名）
        
        #4.保存新的MD5值到文件中
        save_md5(md5_str)
        return f"文件 {filename} 上传成功"

if __name__ == "__main__":
    service = KnowledgeBaseService()
    r = service.upload_by_str("syy减肥就是要少吃多练", "test.txt")
    print(r)
    