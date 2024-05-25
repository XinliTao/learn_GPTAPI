#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 01限定输出格式.py
@time: 2024/5/20 12:04
@software: PyCharm
"""
import json
from openai import OpenAI
from src.utils import get_api


def main(api_key, base_url):
    client = OpenAI(api_key=api_key, base_url=base_url)
    prompt = f"""
    生成一个由三个虚构的订单信息所组成的列表，以JSON格式进行返回。
    JSON列表里的每个元素包含以下信息：
    order_id、customer_name、order_item、phone。
    所有信息都是字符串。
    除了JSON之外，不要输出任何额外的文本。
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    content = response.choices[0].message.content
    return json.loads(content)


if __name__ == '__main__':
    res = main(**get_api('course_giveaway'))
    # res = main(**get_api('my_own'))
    # 使用 json.dumps 方法格式化 JSON 对象
    formatted_res = json.dumps(res, indent=4)
    print(formatted_res)
