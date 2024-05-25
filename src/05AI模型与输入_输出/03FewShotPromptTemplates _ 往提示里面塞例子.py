#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 03FewShotPromptTemplates _ 往提示里面塞例子.py
@time: 2024/5/21 12:37
@software: PyCharm
"""
from langchain_openai import ChatOpenAI
# FewShotChatMessagePromptTemplate 可以帮我们提高构建模型输入的效率
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from src.utils import get_api


def main(api_key, base_url):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "格式化以下客户信息：\n姓名 -> {customer_name}\n年龄 -> {customer_age}\n 城市 -> {customer_city}"),
            ("ai", "##客户信息\n- 客户姓名：{formatted_name}\n- 客户年龄：{formatted_age}\n- 客户所在地：{formatted_city}")
        ]
    )
    examples = [
        {
            "customer_name": "张三",
            "customer_age": "27",
            "customer_city": "长沙",
            "formatted_name": "张三",
            "formatted_age": "27岁",
            "formatted_city": "湖南省长沙市"
        },
        {
            "customer_name": "李四",
            "customer_age": "42",
            "customer_city": "广州",
            "formatted_name": "李四",
            "formatted_age": "42岁",
            "formatted_city": "广东省广州市"
        },
    ]
    """得到一个小样本示范模板"""
    few_shot_template = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    """传给模型的最后消息应该是用户消息"""
    final_prompt_template = ChatPromptTemplate.from_messages(
        # 不仅可以接收元组作为小消息列表的元素，也接收提示模板作为元素
        [
            few_shot_template,
            ("human", "{input}"),
        ]
    )
    final_prompt = final_prompt_template.invoke(
        {"input": "格式化以下客户信息：\n姓名 -> 王五\n年龄 -> 31\n 城市 -> 郑州'"}
    )
    print(final_prompt.messages)

    response = model.invoke(final_prompt)
    print(response.content)


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
