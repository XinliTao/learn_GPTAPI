#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 02ConversationChain _ 开箱即用带记忆的对话链.py
@time: 2024/5/22 15:47
@software: PyCharm
"""
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.utils import get_api


def main(api_key, base_url):
    # return_messages为true，这样存储的那些消息才是列表，而不是一整砣字符串
    memory = ConversationBufferMemory(return_messages=True)
    # 构建模型和链
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)

    """传入模型和记忆"""
    chain = ConversationChain(llm=model, memory=memory)

    res = chain.invoke({"input": "你好，我的名字是粒粒"})
    print(res, res['input'], res['response'], sep="\n")
    res = chain.invoke({"input": "我告诉过你我的名字，是什么？"})
    print(res, res['input'], res['response'], sep="\n")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个脾气暴躁的助手，喜欢冷嘲热讽和用阴阳怪气的语气回答问题。"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    memory = ConversationBufferMemory(return_messages=True)
    """传入模型、记忆和提示模板"""
    chain = ConversationChain(llm=model, memory=memory, prompt=prompt)

    res = chain.invoke({"input": "今天天气怎么样？"})
    print(res, res['input'], res['response'], sep="\n")
    res = chain.invoke({"input": "你记得我问的上一个问题不，是什么？"})
    print(res, res['input'], res['response'], sep="\n")


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
