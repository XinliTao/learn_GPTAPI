#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: main.py
@time: 2024/5/24 11:59
@software: PyCharm
"""
import pandas as pd
import streamlit as st
from utils import dataframe_agent


def create_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    # 把第一个列作为索引，用来表示图表的横轴
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)


def web():
    st.title("💡 CSV数据分析智能工具")

    with st.sidebar:
        openai_api_key = st.text_input("请输入OpenAI API密钥：", type="password")
        openai_base_url = st.text_input("请输入Base URL：", type="default")
        st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

    data = st.file_uploader("上传你的数据文件（CSV格式）：", type="csv")
    if data:
        # 把df储存到会话状态里
        st.session_state["df"] = pd.read_csv(data)
        with st.expander("原始数据"):  # 防止表格占用页面面积过大，放入折叠组件
            st.dataframe(st.session_state["df"])

    # text_area可以比text_input输入更多的内容
    query = st.text_area("请输入你关于以上表格的问题，或数据提取请求，或可视化要求（支持散点图、折线图、条形图）：")
    button = st.button("生成回答")

    if button and not openai_api_key:
        st.info("请输入你的OpenAI API密钥")
    if button and not openai_base_url:
        st.info("请输入你的Base URL")
        st.stop()
    if button and "df" not in st.session_state:
        st.info("请先上传数据文件")
    if button and openai_api_key and "df" in st.session_state:
        with st.spinner("AI正在思考中，请稍等..."):
            response_dict = dataframe_agent(st.session_state["df"], query, openai_api_key, openai_base_url)
            if "answer" in response_dict:
                st.write(response_dict["answer"])
            if "table" in response_dict:
                st.table(pd.DataFrame(response_dict["table"]["data"], columns=response_dict["table"]["columns"]))
            if "bar" in response_dict:
                create_chart(response_dict["bar"], "bar")
            if "line" in response_dict:
                create_chart(response_dict["line"], "line")
            if "scatter" in response_dict:
                create_chart(response_dict["scatter"], "scatter")


if __name__ == '__main__':
    web()
