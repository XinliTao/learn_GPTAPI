#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 03Text Embedding _ 文本变数字？神奇的嵌入向量.py
@time: 2024/5/22 21:42
@software: PyCharm
"""
from langchain_openai import OpenAIEmbeddings

from src.utils import get_api


def main(api_key, base_url):
    # 可以通过dimensions参数指定嵌入向量的维度
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=api_key, openai_api_base=base_url)

    embedded_result = embeddings_model.embed_documents(["Hello world!", "Hey bro"])

    # 传入的每个字符串都会被转化为一个向量
    print("输入列表长度：", len(embedded_result))
    # 列表里面的每个元素还是列表（数字列表）
    print("embedded后的结果：", embedded_result)
    # 数字列表的长度对应向量的维度
    print("模型定义的向量维度：", len(embedded_result[0]))

    # 如果希望嵌入向量维度更小，可以通过dimensions参数进行指定
    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=1024,
                                        openai_api_key=api_key, openai_api_base=base_url)
    embedded_result = embeddings_model.embed_documents(["Hello world!", "Hey bro"])
    print("自己定义的向量维度：", len(embedded_result[0]))


if __name__ == '__main__':
    main(**get_api("course_giveaway"))
