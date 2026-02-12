from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人，可以作诗"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "请你作一首唐诗"),
    ]
)

history_data = [
    ("human", "请你作一首关于春天的诗"),
    ("ai", "窗前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human", "好诗！请你再作一首关于夏天的诗"),
    ("ai", "接天莲叶无穷碧，映日荷花别样红。"),
]


model = ChatTongyi(model="qwen3-max")

#组成链:要求每个组件都是Runnable接口的子类
chain = chat_prompt_template | model

#通过链去调用invoke或stream
res = chain.invoke({"history": history_data})
print(res.content)

#通过stream流式输出
for chunk in chain.stream({"history": history_data}):
    print(chunk.content, end='', flush=True)



