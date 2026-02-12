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

#StringPromptValue
prompt_text = chat_prompt_template.invoke({"history": history_data})
print(prompt_text)

model = ChatTongyi(model="qwen3-max")

res = model.invoke(prompt_text)
print(res.content)


