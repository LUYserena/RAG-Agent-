import os, json
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from typing import Sequence, List
from langchain_core.messages import BaseMessage
from langchain_core.runnables.history import RunnableWithMessageHistory


# message_to_dict：单个消息对象（BaseMessage类实例） -> 字典
# messages_from_dict : [字典fdcyu                                           86t, 字典] -> [消息, 消息] 消息对象列表（BaseMessage类实例列表）
# AIMessage, HumanMessage, SystemMessage 都是 BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id:str, storage_path: str):
        self.session_id = session_id # 会话id
        self.storage_path = storage_path #不同会话id的存储文件，所在的文件夹路径
        
        self.file_path = os.path.join(self.storage_path, self.session_id )
        
        #确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
    
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages) #已有的消息列表
        all_messages.extend(messages) #添加新的消息列表
        
        """添加消息到文件中"""
        #类对象写入文件 -> 二进制
        #可以将BaseMessage对象转换为字典，再将字典转换为json字符串写入文件
        #官方message_to_dict函数：BaseMessage对象 -> 字典
        new_messages = [message_to_dict(m) for m in all_messages] #消息对象列表 -> 字典列表
        
        #将数据写入文件
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(new_messages, f)
    
    @property   # @property装饰器将messages方法编程成员属性用
    def messages(self) -> List[BaseMessage]:
        """从文件中读取消息"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                messages_dict = json.load(f) #读取字典列表
                return messages_from_dict(messages_dict) #字典列表 -> 消息对象列表
        except FileNotFoundError:
            return []
    
    def clear(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
        

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


def get_history(session_id):
    return FileChatMessageHistory(
        session_id=session_id,
        storage_path="./chat_histories" #不同会话id的存储文件，所在的文件夹路径
    )

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
    # res = conversation_chain.invoke({"input": "小明有两个猫"}, session_config)
    # print("第1次执行", res)
    
    # res = conversation_chain.invoke({"input": "小刚有三个狗"}, session_config)
    # print("第2次执行", res)
    
    res = conversation_chain.invoke({"input": "总共有多少个宠物"}, session_config)
    print("第3次执行", res)