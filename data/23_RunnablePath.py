from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough


model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料:{context}。"),
        ("user", "用户提问: {input}")
    ]
)

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(model="text-embedding-v4")
)

#准备一下资料（向量库数据）
# add_texts 传入一个 list[str]
vector_store.add_texts([
    "减肥就是要少吃多练",
    "在减脂期间吃东西很重要，清淡少油控制卡路里摄入并运动起来",
    "跑步是很好的运动哦"
])

input_text = "怎么减肥"

#langchain中的向量存储对象，有一个方法：as_retriever()，可以把向量存储对象转化为Runnable接口的子类对象实例
retriver = vector_store.as_retriever(search_kwargs={"k":2}) #匹配两个对象

def format_func(docs: list[Document]):
    if not docs:
        return "没有找到相关资料"
    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"

    return formatted_str
    
def print_prompt(prompt):
    print(prompt.to_string())
    print("------")
    return prompt
    
#chain
chain = (
    {"input" : RunnablePassthrough(), "context": retriver | format_func} | prompt | print_prompt| model | StrOutputParser()
)

res = chain.invoke(input_text)

print(res)

'''
retriver:
    输入：用户的提问 Str
    输出：向量库的检索结果 List[Document] (没有用户的提问)

prompt:
    输入：用户的提问 + 向量库的检索结果 dict
    输出：最终的提示词 PromptValue
'''
