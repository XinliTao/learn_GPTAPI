#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 01Document Loader _ 把外部文档加载进来.py
@time: 2024/5/22 21:09
@software: PyCharm
"""
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WikipediaLoader


def load_txt():
    loader = TextLoader("demo.txt", encoding="utf-8")
    docs = loader.load()
    print(docs)
    # 查看第一个Document元素的文本内容
    print(docs[0].page_content)


def load_pdf():
    loader = PyPDFLoader("论文介绍.pdf")
    docs = loader.load()
    print(docs)
    # 查看第一个Document元素的文本内容
    print(docs[0].page_content)


def load_wikipedia():
    loader = WikipediaLoader(query="颐和园", load_max_docs=3, lang="zh")
    docs = loader.load()
    print(docs)
    # 查看第一个Document元素的文本内容
    print(docs[0].page_content)


def main():
    print("**********************加载TXT文档**********************")
    load_txt()
    print("**********************加载PDF文档**********************")
    load_pdf()
    print("**********************加载维基百科词条**********************")
    load_wikipedia()


if __name__ == '__main__':
    main()
