"""

基于Streamlit完成WEB网页上传服务
"""

import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

#添加网页标题
st.title("知识库更新服务")

#file_uploader组件，允许用户上传文件
uploader_file = st.file_uploader("请上传txt文件", 
                                 type=["txt"],
                                 accept_multiple_files=False)

service = KnowledgeBaseService() #创建知识库服务对象
# session_state是Streamlit提供的一个全局字典对象，可以在不同的交互中保存和共享数据
if "service" not in st.session_state:
    st.session_state["service"] = service #初始化知识库服务对象到session_state中
    
if uploader_file is not None:
    #提取文件的信息
    file_name = uploader_file.name
    file_size = uploader_file.size / 1024 #转换为KB
    file_type = uploader_file.type
    
    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")
    
    #get_value -> bytes -> decode("utf-8") -> str
    text = uploader_file.getvalue().decode("utf-8")

    with st.spinner("正在上传文件到知识库..."): #在spinner内的代码执行过程中，会有一个转圈动画
        time.sleep(1) #模拟上传过程中的等待时间
        res = st.session_state["service"].upload_by_str(text, file_name) #调用知识库服务对象的upload_by_str方法上传数据到知识库

        st.write(res)