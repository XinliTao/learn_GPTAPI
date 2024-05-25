#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: main.py
@time: 2024/5/21 15:54
@software: PyCharm
"""
import streamlit as st
from utils import generate_script


def web():
    st.title("🎬 视频脚本生成器")

    with st.sidebar:
        openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
        openai_base_url = st.text_input("请输入Base URL：", type="default")
        st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

    subject = st.text_input("💡 请输入视频的主题")
    video_length = st.number_input("⏱️ 请输入视频的大致时长（单位：分钟）", min_value=0.1, step=0.1)
    creativity = st.slider("✨ 请输入视频脚本的创造力（数字小说明更严谨，数字大说明更多样）", min_value=0.0,
                           max_value=1.0, value=0.2, step=0.1)
    submit = st.button("生成脚本")

    if submit and not openai_api_key:
        st.info("请输入你的OpenAI API密钥")
        st.stop()
    if submit and not openai_base_url:
        st.info("请输入你的Base URL")
        st.stop()
    if submit and not subject:
        st.info("请输入视频的主题")
        st.stop()
    if submit and not video_length >= 0.1:
        st.info("视频长度需要大于或等于0.1")
        st.stop()
    if submit:
        with st.spinner("AI正在思考中，请稍等..."):
            search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key, openai_base_url)
        st.success("视频脚本已生成！")
        st.subheader("🔥 标题：")
        st.write(title)
        st.subheader("📝 视频脚本：")
        st.write(script)
        with st.expander("维基百科搜索结果 👀"):
            st.info(search_result)


if __name__ == '__main__':
    # 启动网站
    web()
