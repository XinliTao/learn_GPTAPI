#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: utils.py
@time: 2024/5/22 17:25
@software: PyCharm
"""
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
# from src.utils import get_api


def get_chat_response(prompt, memory, api_key, base_url):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)
    # 使用对话链的好处是：它能自动帮我们加载记忆，以及把新对话加入记忆，不需要手动做（容易遗漏和出错）
    chain = ConversationChain(llm=model, memory=memory)

    response = chain.invoke({"input": prompt})
    return response["response"]


if __name__ == '__main__':
    memory_test = ConversationBufferMemory(return_messages=True)
    print(get_chat_response("牛顿提出过哪些知名的定律？", memory_test, **get_api("course_giveaway")))
    print(get_chat_response("我上一个问题是什么？", memory_test, **get_api("course_giveaway")))
