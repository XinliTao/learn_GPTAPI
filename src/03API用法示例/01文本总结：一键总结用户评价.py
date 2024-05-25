#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 01文本总结：一键总结用户评价.py
@time: 2024/5/20 17:00
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
    product_review = """
    我上个月买的这个多功能蓝牙耳机。它的连接速度还挺快，而且兼容性强，无论连接手机还是笔记本电脑，基本上都能快速配对上。
    音质方面，中高音清晰，低音效果震撼，当然这个价格来说一分钱一分货吧，毕竟也不便宜。
    耳机的电池续航能力不错，单次充满电可以连续使用超过8小时。
    不过这个耳机也有一些我不太满意的地方。首先是在长时间使用后，耳廓有轻微的压迫感，这可能是因为耳套的材料较硬。总之我感觉戴了超过4小时后耳朵会有点酸痛，需要摘下休息下。
    而且耳机的防水性能不是特别理想，在剧烈运动时的汗水防护上有待加强。
    最后是耳机盒子的开合机制感觉不够紧致，有时候会不小心打开。
    """
    product_review_prompt = f"""
    你的任务是为用户对产品的评价生成简要总结。
    请把总结主要分为两个方面，产品的优点，以及产品的缺点，并以Markdown列表形式展示。
    用户的评价内容会以三个#符号进行包围。

    ###
    {product_review}
    ###
    """
    response = get_openai_response(client, product_review_prompt)
    print(response)


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
