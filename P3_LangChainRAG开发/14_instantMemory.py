from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatTongyi(model="qwen3-max")
# prompt = PromptTemplate.from_template(
#     "你需要根据对话历史回应用户问题。对话历史：{chat_history}。用户当前输入：{input}， 请给出回应"
# )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据对话历史回应用户问题。对话历史："),
         MessagesPlaceholder("chat_history"),
         ("human", "请回答如下问题：{input}")
    ]
)

str_parser = StrOutputParser()

base_chain = prompt | model | str_parser

history_store = {} #用于存储会话id和对应的InMemoryChatMessageHistory对象

#实现通过会话id获取InMemoryChatMessageHistory对象的函数
def get_history(session_id):
    #在实际应用中，你可能需要从数据库或其他存储中获取历史消息
    #这里我们使用一个简单的字典来模拟存储
    if session_id not in history_store:
        history_store[session_id] = InMemoryChatMessageHistory()
    return history_store[session_id]

#创建一个新的链，对原有链增强功能，自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain, #被增强的原有链
    get_history, #通过会话id获取RunnableWithMessageHistory类对象
    input_messages_key="input", #用户输入消息在模板中的占位符
    history_messages_key="chat_history" #历史消息在模板中的占位符
)

if __name__ == "__main__":
    #固定格式：添加langchain的配置，为当前程序配置所属的conversation_id
    session_config = {
        "configurable": {
            "session_id": "user_001" #为当前程序配置所属的conversation_id
        }
    }
    res = conversation_chain.invoke({"input": "小明有两个猫"}, session_config)
    print("第1次执行", res)
    
    res = conversation_chain.invoke({"input": "小刚有三个狗"}, session_config)
    print("第2次执行", res)
    
    res = conversation_chain.invoke({"input": "总共有多少个宠物"}, session_config)
    print("第3次执行", res)