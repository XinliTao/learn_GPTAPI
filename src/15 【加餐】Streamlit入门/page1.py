#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: page1.py
@time: 2024/5/25 11:12
@software: PyCharm
"""
import streamlit as st
import pandas as pd


def web():
    # 支持markdown语法
    st.title("我的个人网站 💡")

    # 自动调用writer方法
    "### 早上好"
    a = 329 * 3
    a
    [11, 22, 33]
    {"a": "1", "b": "2", "c": 3}

    st.image("src/15 【加餐】Streamlit入门/头像.jpg", width=200)

    df = pd.DataFrame({"学号": ["01", "02", "03", "04", "05"],
                       "班级": ["二班", "一班", "二班", "三班", "一班"],
                       "成绩": [92, 67, 70, 88, 76]})
    # 此时表格是交互式的，有排序、搜索之类的功能
    st.dataframe(df)
    st.divider()
    # 此时表格不是交互式的
    st.table(df)


if __name__ == '__main__':
    web()
