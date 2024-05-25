#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 03思维链与分步骤思考.py
@time: 2024/5/20 12:48
@software: PyCharm
"""
from openai import OpenAI
from src.utils import get_api


def ask_directly(client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "该组中的奇数加起来为偶数：4、8、9、15、12、2、1，对吗？"
            },
            {
                "role": "assistant",
                "content": "所有奇数相加等于25。答案为否。"
            },
            {
                "role": "user",
                "content": "该组中的奇数加起来为偶数：17、10、19、4、8、12、24，对吗？"
            },
            {
                "role": "assistant",
                "content": "所有奇数相加等于36。答案为是。"
            },
            {
                "role": "user",
                "content": "该组中的奇数加起来为偶数：15、12、5、3、72、17、1，对吗？"
            },
        ]
    )
    return response.choices[0].message.content


def chain_of_thought(client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "该组中的奇数加起来为偶数：4、8、9、15、12、2、1，对吗？"
            },
            {
                "role": "assistant",
                "content": "所有奇数（9、15、1）相加，9 + 15 + 1 = 25。答案为否。"
            },
            {
                "role": "user",
                "content": "该组中的奇数加起来为偶数：17、10、19、4、8、12、24，对吗？"
            },
            {
                "role": "assistant",
                "content": "所有奇数（17、19）相加，17 + 19 = 36。答案为是。"
            },
            {
                "role": "user",
                "content": "该组中的奇数加起来为偶数：15、12、5、3、72、17、1，对吗？"
            },
        ]
    )
    return response.choices[0].message.content


def think_in_steps(client):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "该组中的奇数加起来为偶数：15、12、5、3、72、17、1，对吗？让我们来分步骤思考。"
            },
        ]
    )
    return response.choices[0].message.content


def main(api_key, base_url):
    client = OpenAI(api_key=api_key, base_url=base_url)
    print("直接询问：\n", ask_directly(client))
    print("思维链：\n", chain_of_thought(client))
    print("分步骤思考：\n", think_in_steps(client))


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
