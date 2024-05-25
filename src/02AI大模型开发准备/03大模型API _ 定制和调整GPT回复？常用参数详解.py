#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 03大模型API _ 定制和调整GPT回复？常用参数详解.py
@time: 2024/5/20 0:59
@software: PyCharm
"""
from openai import OpenAI
from src.utils import get_api


def max_tokens(client):
    """返回的最大token长度，超过就截断"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "四大文明古国分别有哪些"
            }
        ],
        max_tokens=100
    )
    print(response.choices[0].message.content)


def temperature(client):
    """改变预测token的分布概率，控制AI回答的随机性（创造性），[0,2]，默认为1"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "四大文明古国分别有哪些"
            }
        ],
        max_tokens=100,
        temperature=2
    )
    print(response.choices[0].message.content)


def top_p(client):
    """从预测的token分布概率中取前面的概率和>=top_p，也能控制回答的随机性和创造性，[0,1]"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "四大文明古国分别有哪些"
            }
        ],
        max_tokens=300,
        top_p=0.4
    )
    print(response.choices[0].message.content)


def frequency_penalty(client):
    """生成内容的重复性，根据词的频率，对重复多的词进行惩罚，[-2,2]，一般在0~1之间。影响生成文本里词重复出现的频率。"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "生成一个购物清单，包含至少20个物品，每个物品之间用逗号进行分隔，例如：苹果，香蕉，牛奶"
            }
        ],
        max_tokens=300,
        # frequency_penalty=-2
        frequency_penalty=2
    )
    print(response.choices[0].message.content)


def presence_penalty(client):
    """生成内容的重复性，所有词一视同仁，进行惩罚，[-2,2]。影响的是生成内容是否包含更多的新词。"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "生成一个购物清单，包含至少20个物品，每个物品之间用逗号进行分隔，例如：苹果，香蕉，牛奶"
            }
        ],
        max_tokens=300,
        presence_penalty=2
    )
    print(response.choices[0].message.content)


def main(api_key, base_url):
    client = OpenAI(api_key=api_key, base_url=base_url)
    print("**********max_tokens**********")
    max_tokens(client)
    print("**********temperature**********")
    temperature(client)
    print("**********top_p**********")
    top_p(client)
    print("**********frequency_penalty**********")
    frequency_penalty(client)
    print("**********presence_penalty**********")
    presence_penalty(client)


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
