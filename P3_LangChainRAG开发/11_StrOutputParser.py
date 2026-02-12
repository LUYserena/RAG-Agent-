from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

parser = StrOutputParser()
model = ChatTongyi(model="qwen3-max")
prompt = PromptTemplate.from_template("我的邻居姓{lastname}，生了个{gender}, 请起名，仅告诉我名字")

chain = prompt | model | parser | model
res = chain.invoke({"lastname":"张", "gender":"女"})
print(res.content)