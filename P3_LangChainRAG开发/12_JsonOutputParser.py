from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

#创建所需的解析器
json_parser = JsonOutputParser()
str_parser = StrOutputParser()

#创建模型
model = ChatTongyi(model="qwen3-max")

#第一个提示提模板
first_prompt = PromptTemplate.from_template(
    "我领居姓： {lastname}, 刚生了{gender}, 请帮忙起名字,仅回复我名字,并封装为json格式返回给我, 要求key是name,value是名字。请严格遵守格式要求返回"
)

#第二个提示词模板
second_prompt = PromptTemplate.from_template(
    "姓名： {name}, 请帮我解析含义"
)

#构建链  
chain = first_prompt | model | json_parser | second_prompt | model | str_parser
# res = chain.invoke({"lastname" : "张", "gender" : "女儿"})



for chunk in chain.stream({"lastname" : "张", "gender" : "女儿"}):
    print(chunk, end="", flush=True)

print(res)
