#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: page6.py
@time: 2024/5/25 14:25
@software: PyCharm
"""
import streamlit as st


def web():
    if "a" not in st.session_state:
        st.session_state.a = 0
    clicked = st.button("加1")
    if clicked:
        st.session_state.a += 1
    st.write(st.session_state.a)
    print(st.session_state)


if __name__ == '__main__':
    web()
