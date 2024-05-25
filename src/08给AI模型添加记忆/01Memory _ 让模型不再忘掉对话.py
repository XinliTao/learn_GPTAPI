#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 01Memory _ 让模型不再忘掉对话.py
@time: 2024/5/22 15:20
@software: PyCharm
"""
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from src.utils import get_api


def main(api_key, base_url):
    # return_messages为true，这样存储的那些消息才是列表，而不是一整砣字符串
    memory = ConversationBufferMemory(return_messages=True)
    # load_memory_variables查看历史记忆，传入空字典
    print(memory.load_memory_variables({}))

    # save_context存储对话，input,output=>human,AI
    memory.save_context({"input": "我的名字是林粒粒"}, {"output": "你好，林粒粒"})
    print(memory.load_memory_variables({}))
    # 再加一轮对话
    memory.save_context({"input": "我是一名程序员"}, {"output": "好的，我记住了"})
    print(memory.load_memory_variables({}))

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个乐于助人的助手。"),
            MessagesPlaceholder(variable_name="history"),  # 历史消息，variable_name参数指代消息列表名，即变量名
            ("human", "{user_input}"),
        ]
    )

    # 构建模型和链
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)
    chain = prompt | model

    user_input = "你知道我的名字吗？"
    history = memory.load_memory_variables({})["history"]
    result = chain.invoke({
        "user_input": "你知道我的名字吗？",
        'history': history
    })
    print(result)
    # 把新一轮的用户提示和AI回应存储到记忆里
    memory.save_context({"input": user_input}, {"output": result.content})
    print(memory.load_memory_variables({}))

    user_input = "根据对话历史告诉我，我上一个问题问你的是什么？请重复一遍"
    history = memory.load_memory_variables({})["history"]
    result = chain.invoke({
        "user_input": user_input,
        'history': history
    })
    print(result)


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
