from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
# Chroma 向量数据区（轻量级）
#
vector_store = Chroma(
    collection_name="my_collection", #当前向量存储的名字，类似数据库的表名字
    embedding_function=DashScopeEmbeddings(), #嵌入函数
    persist_directory="./chroma_db" #指定数据存放的文件夹，持久化目录，存储向量数据
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column = "source", #指定本条数据来源是哪里
)

documents = loader.load()

#向量存储的新增 删除 检索
vector_store.add_documents(
    documents=documents, #被添加的文档，类型：list[Document]
    ids=["id" + str(i) for i in range(1, len(documents)+1)] #给添加的文档提供id(字符串) list[str]
)

#删除 传入[id, id....]
vector_store.delete(["id1", "id2"])

#检索 返回类型 list[Document]
result = vector_store.similarity_search(
    query="python是不是简单易学啊", #查询文本
    k=3, #返回最相似的k个文档
    filter={"source": "黑马程序员"} #过滤条件，指定只检索来源于黑马程序员v的数据
)

print(result)