#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: main.py
@time: 2024/5/22 17:30
@software: PyCharm
"""
import streamlit as st
from langchain.memory import ConversationBufferMemory

from utils import get_chat_response


def web():
    st.title("💬 克隆ChatGPT")

    with st.sidebar:
        openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
        openai_base_url = st.text_input("请输入Base URL：", type="default")
        st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")
        submit = st.button("清空对话")

    # 是否清空对话
    if submit:
        st.session_state.pop("memory")

    # 初始化记忆
    if "memory" not in st.session_state:
        st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
        st.session_state["messages"] = [{"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]

    # 在页面上展示过往的对话
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])

    # 提示模板输入框，返回的是用户输入回车之后的字符串
    prompt = st.chat_input()
    if prompt:
        if not openai_api_key:
            st.info("请输入你的OpenAI API Key")
            st.stop()
        if not openai_base_url:
            st.info("请输入你的Base URL")
            st.stop()
        # 把本次用户提问的信息输出在记忆中和网页上，格式应保持一致
        st.session_state["messages"].append({"role": "human", "content": prompt})
        st.chat_message("human").write(prompt)

        with st.spinner("AI正在思考中，请稍等..."):
            response = get_chat_response(prompt, st.session_state["memory"], openai_api_key, openai_base_url)
        msg = {"role": "ai", "content": response}
        st.session_state["messages"].append(msg)
        st.chat_message("ai").write(response)


if __name__ == '__main__':
    web()
