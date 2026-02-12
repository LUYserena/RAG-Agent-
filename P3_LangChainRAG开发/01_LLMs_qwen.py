from langchain_community.llms.tongyi import Tongyi
import os

api_key=os.getenv("OPENAI_API_KEY")
#qwen3-max是chat模型，qwen-max是基础模型
model = Tongyi(model="qwen-max")

#调用invoke向模型提问
res = model.invoke(input="你是谁呀，能做什么？")
print(res)