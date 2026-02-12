from langchain_community.chat_models.tongyi  import ChatTongyi
from langchain_core.messages import (HumanMessage, SystemMessage, AIMessage)

#得到模型对象，qwen3-max是chat模型
model = ChatTongyi(model="qwen3-max")

#准备消息列表
messages = [
    SystemMessage(content="你是一个边塞诗人"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    HumanMessage(content="按照上一个回复的格式，再写一首关于春天的诗")
]

#调用stream流式执行
res = model.stream(input=messages)

#打印流式输出结果
for chunk in res:
    print(chunk.content, end='', flush=True)