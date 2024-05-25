#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 01玩转AI聊天模型.py
@time: 2024/5/21 0:37
@software: PyCharm
"""
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage

from src.utils import get_api


def main(api_key, base_url):
    """
    请注意，如果你使用的是课程提供的API，需要额外指定 openai_api_base，比如：
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       openai_api_key = "<你的API密钥>",
                       openai_api_base = "https://api.aigc369.com/v1")
    """

    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)

    """model = ChatOpenAI(
        # 常用参数可以直接作为可选参数进行设置
        model="gpt-3.5-turbo",
        temperature=1.2,
        max_tokens=500,
        model_kwargs={  # 不常用的参数可以键值对的方式指定原生api的其他参数，详情参考langchain官网
            "frequency_penalty": 1.1
        }
    )"""
    messages = [
        # SystemMessage=>系统消息，HumanMessage=>用户消息，AIMessage=>AI消息
        SystemMessage(content="请你作为我的物理课助教，用通俗易懂且间接的语言帮我解释物理概念。"),
        HumanMessage(content="什么是波粒二象性？"),
    ]
    response = model.invoke(messages)
    print(response)
    print(response.content)


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
