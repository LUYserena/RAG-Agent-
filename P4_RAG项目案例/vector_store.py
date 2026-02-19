from langchain_chroma import Chroma
import config_data as config
class VectorStoreService(object):
    def __init__(self, embedding):
        """
        param embedding: 嵌入模型的传入
        """
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )
    
    def get_retirver(self):
        """
        获取向量检索器,方便传入chain
        """
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold}) #返回一个向量检索器对象，search_kwargs参数指定了搜索时返回的结果数量

if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    embedding = DashScopeEmbeddings(model="text-embedding-v4")
    service = VectorStoreService(embedding)
    retriever = service.get_retirver()
    
    res = retriever.invoke("我的体重120斤，请推荐尺码")
    print(res)
   