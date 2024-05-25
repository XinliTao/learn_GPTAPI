#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: page2.py
@time: 2024/5/25 11:24
@software: PyCharm
"""
import streamlit as st


def web():
    name = st.text_input("请输入你的名字：")
    if name:
        st.write(f"你好，{name}")
    st.divider()

    password = st.text_input("请输入你的密码：", type="password")
    st.divider()

    paragraph = st.text_area("请输入一段自我介绍：")
    st.divider()

    age = st.number_input("请输入你的年龄：", value=20, min_value=0, max_value=150, step=1)
    st.write(f"你的年龄是：{age}岁")
    st.divider()

    checked = st.checkbox("我同意以上条款")
    if checked:
        st.write("感谢你的同意！")
    st.divider()

    submitted = st.button("提交")
    if submitted:
        st.write("提交成功！")


if __name__ == '__main__':
    web()
