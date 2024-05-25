#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 02零样本VS小样本.py
@time: 2024/5/20 12:19
@software: PyCharm
"""
from openai import OpenAI
from src.utils import get_api


def zero_sample(client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "格式化以下信息：\n姓名 -> 张三\n年龄 -> 27\n客户ID -> 001"
            }
        ]
    )
    return response.choices[0].message.content


def small_sample(client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "格式化以下信息：\n姓名 -> 张三\n年龄 -> 27\n客户ID -> 001"
            },
            {
                "role": "assistant",
                "content": "##客户信息\n- 客户姓名：张三\n- 客户年龄：27岁\n- 客户ID：001"
            },
            {
                "role": "user",
                "content": "格式化以下信息：\n姓名 -> 李四\n年龄 -> 42\n客户ID -> 002"
            },
            {
                "role": "assistant",
                "content": "##客户信息\n- 客户姓名：李四\n- 客户年龄：42岁\n- 客户ID：002"
            },
            {
                "role": "user",
                "content": "格式化以下信息：\n姓名 -> 王五\n年龄 -> 32\n客户ID -> 003"
            }
        ]
    )
    return response.choices[0].message.content


def main(api_key, base_url):
    client = OpenAI(api_key=api_key, base_url=base_url)
    print("零样本提示：\n", zero_sample(client))
    print("小样本提示：\n", small_sample(client))


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
