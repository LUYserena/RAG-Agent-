from langchain_community.llms.tongyi import Tongyi
import os

api_key=os.getenv("OPENAI_API_KEY")
#qwen3-max是chat模型，qwen-max是基础模型
model = Tongyi(model="qwen-max", streaming=True)

#stream方法获得流式输出
res = model.stream(input="你是谁呀，能做什么？")
for chunk in res:
    print(chunk, end='', flush=True)