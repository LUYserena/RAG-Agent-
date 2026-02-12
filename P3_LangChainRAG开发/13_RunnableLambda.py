from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

str_parser = StrOutputParser()

#创建模型
model = ChatTongyi(model="qwen3-max")

#第一个提示提模板
first_prompt = PromptTemplate.from_template(
    "我领居姓： {lastname}, 刚生了{gender}, 请帮忙起名字,仅回复我名字,不需要额外信息"
)

#第二个提示词模板
second_prompt = PromptTemplate.from_template(
    "姓名： {name}, 请帮我解析含义"
)

#函数的入参：AIMessage -> dict
my_func = RunnableLambda(
    lambda x: {"name": x.content}
)

chain = first_prompt | model | my_func | second_prompt | model | str_parser
for chunk in chain.stream({"lastname" : "张", "gender" : "男孩"}):
    print(chunk, end="", flush=True)