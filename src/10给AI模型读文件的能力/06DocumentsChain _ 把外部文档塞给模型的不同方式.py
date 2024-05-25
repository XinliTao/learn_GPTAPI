#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 06DocumentsChain _ 把外部文档塞给模型的不同方式.py
@time: 2024/5/23 0:17
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


def turn_on_model(model, memory, retriever, chain_type):
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory,
        chain_type=chain_type
    )
    return qa.invoke({"chat_history": memory, "question": "卢浮宫这个名字怎么来的？"})


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

    # 所有片段给模型叫做Stuff(填充方式)
    res = turn_on_model(model, memory, retriever, "stuff")
    print("stuff:\n", res)
    # Map-Reduce（映射归约）： 先Map把每个片段和问题分别得到一个结果，Reduce阶段把这些结果形成统一的信息集合，模型最后得到一个连贯的、结合了多方面信息的回答
    res = turn_on_model(model, memory, retriever, "map_reduce")
    print("map_reduce:\n", res)
    # Refine（优化）：从第一个片段开始得到模型针对查询的回答，把回答连带查询和第二个片段给模型对回答进行优化，直至最后一个片段
    res = turn_on_model(model, memory, retriever, "refine")
    print("refine:\n", res)
    # Map-Rerank（映射-重新排序）：Map和Map-Reduce一样，但是会要求模型对每个片段的回答做出评估打分，Rerank阶段系统把得分最高的作为最终回答
    res = turn_on_model(model, memory, retriever, "map_rerank")
    print("map_rerank:\n", res)


if __name__ == '__main__':
    main(**get_api("course_giveaway"))
