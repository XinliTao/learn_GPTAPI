#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 04Vector Store _ 给AI模型加海马体.py
@time: 2024/5/22 21:55
@software: PyCharm
"""
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.utils import get_api


def main(api_key, base_url):
    # 加载数据
    loader = TextLoader("src/10给AI模型读文件的能力/demo.txt", encoding="utf-8")
    docs = loader.load()
    # 把文本分为块
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=40,
        separators=["\n\n", "\n", "。", "！", "？", "，", "、", ""]
    )

    # 切割后的文本列表
    texts = text_splitter.split_documents(docs)
    # 创建一个嵌入模型的实例
    embeddings_model = OpenAIEmbeddings(openai_api_key=api_key, openai_api_base=base_url)

    # 构建向量数据库库
    db = FAISS.from_documents(texts, embeddings_model)
    # 拿到一个检索器，从大量文本中快速检索相关信息的组件，也实现了Runnable接口，具有invoke方法
    retriever = db.as_retriever()

    # 返回一个Document类组成的列表，越相似的文本块在越前面
    retrieved_docs = retriever.invoke("卢浮宫这个名字怎么来的？")
    print("*********************卢浮宫这个名字怎么来的？*********************")
    print(retrieved_docs[0].page_content, end="\n\n")

    retrieved_docs = retriever.invoke("卢浮宫在哪年被命名为中央艺术博物馆？")
    print("*********************卢浮宫在哪年被命名为中央艺术博物馆？*********************")
    print(retrieved_docs[0].page_content, end="\n\n")


if __name__ == '__main__':
    main(**get_api("course_giveaway"))
