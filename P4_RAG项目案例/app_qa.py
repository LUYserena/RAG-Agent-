import streamlit as st
import time  
from rag import RagService
import config_data as config

#标题
st.title("智能客服")
st.divider() #分隔符


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "你好呀，有什么可以帮你？"}] #初始化消息列表

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()
    
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"]) #在页面输出消息
    
#在页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:
    #在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt}) #将用户消息添加到消息列表中
    
    ai_res_list = [] #用于存储AI的回答内容
    with st.spinner("正在思考..."):
        #在页面输出AI的回答
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, {"configurable": {"session_id": config.session_config["configurable"]["session_id"]}})
        
        #yield
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["messages"].append({"role": "assistant", "content": "".join(ai_res_list)}) #将用户消息添加到消息列表中
    
