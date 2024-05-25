#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 02大模型API _ GPT模型咋收费？必了解的token计数.py
@time: 2024/5/20 0:25
@software: PyCharm
"""
import tiktoken


def main():
    # 传入模型名，得到对应的编码器
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    print(encoding)

    print(encoding.encode("黄河之水天上来"))

    return len(encoding.encode("黄河之水天上来"))


if __name__ == '__main__':
    token_length = main()

    print("当前句子的token长度为：", token_length)
