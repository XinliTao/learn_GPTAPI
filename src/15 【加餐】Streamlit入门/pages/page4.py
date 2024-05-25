#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: page4.py
@time: 2024/5/25 14:25
@software: PyCharm
"""
import streamlit as st


def web():
    with st.sidebar:
        name = st.text_input("请输入你的名字：")
        if name:
            st.write(f"你好，{name}")

    column1, column2, column3 = st.columns([1, 2, 3])  # 各个数字大小代表所占宽度大小
    with column1:
        password = st.text_input("请输入你的密码：", type="password")

    with column2:
        paragraph = st.text_area("请输入一段自我介绍：")

    with column3:
        age = st.number_input("请输入你的年龄：", value=20, min_value=0, max_value=150, step=1)
        st.write(f"你的年龄是：{age}岁")

    checked = st.checkbox("我同意以上条款")
    if checked:
        st.write("感谢你的同意！")

    st.divider()
    submitted = st.button("提交")
    if submitted:
        st.write("提交成功！")


if __name__ == '__main__':
    web()
