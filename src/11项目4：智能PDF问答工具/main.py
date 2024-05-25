#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: main.py
@time: 2024/5/23 0:53
@software: PyCharm
"""
import streamlit as st

from langchain.memory import ConversationBufferMemory
from utils import qa_agent


def web():
    st.title("📑 AI智能PDF问答工具")

    with st.sidebar:  # 创建侧边栏
        openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
        openai_base_url = st.text_input("请输入Base URL：", type="default")
        st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

    if "memory" not in st.session_state:  # 当会话状态没有memory
        st.session_state["memory"] = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="answer"
        )

    uploaded_file = st.file_uploader("上传你的PDF文件：", type="pdf")
    question = st.text_input("对PDF的内容进行提问", disabled=not uploaded_file)

    if uploaded_file and question and not openai_api_key:
        st.info("请输入你的OpenAI API密钥")
    if uploaded_file and question and not openai_base_url:
        st.info("请输入你的Base URL")
        st.stop()

    if uploaded_file and question and openai_api_key and openai_base_url:
        with st.spinner("AI正在思考中，请稍等..."):
            response = qa_agent(openai_api_key, openai_base_url, st.session_state["memory"],
                                uploaded_file, question)
        st.write("### 答案")
        st.write(response["answer"])
        st.session_state["chat_history"] = response["chat_history"]

    if "chat_history" in st.session_state:
        with st.expander("历史消息"):
            for i in range(0, len(st.session_state["chat_history"]), 2):
                human_message = st.session_state["chat_history"][i]
                ai_message = st.session_state["chat_history"][i + 1]
                # 使用chat_message比write更直观
                st.chat_message("human").write(human_message.content)
                st.chat_message("ai").write(ai_message.content)
                if i < len(st.session_state["chat_history"]) - 2:
                    st.divider()


if __name__ == '__main__':
    web()
