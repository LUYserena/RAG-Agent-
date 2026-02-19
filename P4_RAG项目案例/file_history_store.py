import os, json
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from typing import Sequence, List
from langchain_core.messages import BaseMessage

def get_history(session_id):
    return FileChatMessageHistory(
        session_id=session_id,
        storage_path="./chat_histories" #不同会话id的存储文件，所在的文件夹路径
    )


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
        