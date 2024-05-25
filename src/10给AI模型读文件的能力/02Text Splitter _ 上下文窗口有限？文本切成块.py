#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 02Text Splitter _ 上下文窗口有限？文本切成块.py
@time: 2024/5/22 21:27
@software: PyCharm
"""
from langchain_community.document_loaders import TextLoader
# 导入字符递归分割器
from langchain_text_splitters import RecursiveCharacterTextSplitter


def main():
    # 加载文档
    loader = TextLoader("./demo.txt", encoding="utf-8")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # 每块文本的最大长度
        chunk_overlap=40,  # 分隔片段之间重叠的长度
        # 用于分割的字符，排在前面的字符优先，如果分割出来的文本仍然超过了设定的最大长度，就选择列表里的下一个分隔符进行分割
        separators=["\n\n", "\n", "。", "！", "？", "，", "、", ""]
    )
    texts = text_splitter.split_documents(docs)

    print(texts)
    # len(texts[0].page_content) <= chunk_size
    print(texts[0].page_content)


if __name__ == '__main__':
    main()
