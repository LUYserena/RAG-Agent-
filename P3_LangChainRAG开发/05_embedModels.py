from langchain_community.embeddings import DashScopeEmbeddings

#创建模型对象，不传model默认使用text-embedding-v1
model = DashScopeEmbeddings()

#不用invoke stream
#embed_query方法获得文本的向量表示
#embed_documents方法获得文档的向量表示
print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你","我讨厌你"]))