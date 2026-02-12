from openai import OpenAI
import os
#1.获取client对象

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

#2.调用模型
response = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": "你是一个python编程助手，并且话有点多"},
        {"role": "assistant", "content": "好的，请问有什么可以帮您？"},
        {"role": "user", "content": "输出1-10的数字，使用python代码实现"},
    ],
    stream=True
)

#3.处理结果
for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)
    #end代表每一段内容不换行，flush代表实时输出内容