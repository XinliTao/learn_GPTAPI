#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 05RetrievalChain _ 开箱即用的索引增强对话链.py
@time: 2024/5/22 23:48
@software: PyCharm
"""
# 带记忆的检索增强生成对话链
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.utils import get_api


def main(api_key, base_url):
    """文档的切割和向量化"""
    loader = TextLoader("src/10给AI模型读文件的能力/demo.txt", encoding="utf-8")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=40,
        separators=["\n", "。", "！", "？", "，", "、", ""]
    )
    texts = text_splitter.split_documents(docs)
    embeddings_model = OpenAIEmbeddings(openai_api_key=api_key, openai_api_base=base_url)
    db = FAISS.from_documents(texts, embeddings_model)
    retriever = db.as_retriever()  # 获取到向量数据库的检索器

    # 创建聊天模型的实例
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)
    # ConversationalRetrievalChain里储存历史消息的变量名叫做chat_history，最后输出的结果里AI模型的输出对应着answer键的值
    memory = ConversationBufferMemory(return_messages=True, memory_key='chat_history', output_key='answer')

    """RAG对话链"""
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )

    question = "卢浮宫这个名字怎么来的？"
    res = qa.invoke({"chat_history": memory, "question": question})
    print(res)

    question = "对应的拉丁语是什么呢？"
    res = qa.invoke({"chat_history": memory, "question": question})
    print(res)

    """希望RAG返回的结果里面有它参考的外部文档里的原片段"""
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory,
        return_source_documents=True  # source_documents字段中，排在越前面的Document代表越相关
    )

    question = "卢浮宫这个名字怎么来的？"
    res = qa.invoke({"chat_history": memory, "question": question})
    print(res)


if __name__ == '__main__':
    main(**get_api("course_giveaway"))
