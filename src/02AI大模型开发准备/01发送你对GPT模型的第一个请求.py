#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 01发送你对GPT模型的第一个请求.py
@time: 2024/5/19 21:58
@software: PyCharm
"""
from openai import OpenAI
from src.utils import get_api


def main(api_key, base_url):
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # 我们给AI的上下文msg列表的token数量不能超过上下文窗口(token数量)，否则会出现报错
            {"role": "system", "content": "你是一个乐于助人、语气友善的AI聊天助手"},
            {"role": "user", "content": "你是谁"},
            {"role": "assistant", "content": "我是ChatGPT，由OpenAI开发的一款大型语言模型。"},
            {"role": "user", "content": "四大文明古国分别有哪些"}
        ]
    )
    return response


if __name__ == '__main__':
    res = main(**get_api('course_giveaway'))
    # res = main(**get_api('my_own'))
    print(res)
    print(res.choices[0].message.content)
