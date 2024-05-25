#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: utils.py
@time: 2024/5/23 0:53
@software: PyCharm
"""
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


def qa_agent(api_key, base_url, memory, uploaded_file, question):
    # 导入模型
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)
    # 把用户上传的文件转为二进制后存入内存file_content变量中
    file_content = uploaded_file.read()
    temp_file_path = "src/11项目4：智能PDF问答工具/temp.pdf"
    # 把文件以二进制写入到temp_file_path
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)
    # 加载文件，拿到加载器实例
    loader = PyPDFLoader(temp_file_path)
    # 加载出Documents列表
    docs = loader.load()
    # 实例化字符递归分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n", "。", "！", "？", "，", "、", ""]
    )
    # 分割文档列表
    texts = text_splitter.split_documents(docs)
    # 实现向量嵌入
    embeddings_model = OpenAIEmbeddings(openai_api_key=api_key, openai_api_base=base_url)
    # 构建向量数据库
    db = FAISS.from_documents(texts, embeddings_model)
    retriever = db.as_retriever()  # 获取检索器
    # 带记忆的检索增强对话链
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )
    response = qa.invoke({"chat_history": memory, "question": question})
    return response
