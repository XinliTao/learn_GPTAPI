#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 03文本分类：客户问题自动归类.py
@time: 2024/5/20 17:12
@software: PyCharm
"""
from openai import OpenAI
from src.utils import get_api


def get_openai_response(client, prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def main(api_key, base_url):
    client = OpenAI(api_key=api_key, base_url=base_url)
    q1 = "我刚买的XYZ智能手表无法同步我的日历，我应该怎么办？"
    q2 = "XYZ手表的电池可以持续多久？"
    q3 = "XYZ品牌的手表和ABC品牌的手表相比，有什么特别的功能吗？"
    q4 = "安装XYZ智能手表的软件更新后，手表变得很慢，这是啥原因？"
    q5 = "XYZ智能手表防水不？我可以用它来记录我的游泳数据吗？"
    q6 = "我想知道XYZ手表的屏幕是什么材质，容不容易刮花？"
    q7 = "请问XYZ手表标准版和豪华版的售价分别是多少？还有没有进行中的促销活动？"
    q_list = [q1, q2, q3, q4, q5, q6, q7]

    category_list = ["产品规格", "使用咨询", "功能比较", "用户反馈", "价格查询", "故障问题", "其它"]

    classify_prompt_template = """
    你的任务是为用户对产品的疑问进行分类。
    请仔细阅读用户的问题内容，给出所属类别。类别应该是这些里面的其中一个：{categories}。
    直接输出所属类别，不要有任何额外的描述或补充内容。
    用户的问题内容会以三个#符号进行包围。

    ###
    {question}
    ###
    """

    for q in q_list:
        formatted_prompt = classify_prompt_template.format(categories="，".join(category_list), question=q)
        response = get_openai_response(client, formatted_prompt)
        print(response)


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
