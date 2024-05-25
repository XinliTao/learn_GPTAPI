#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 04文本翻译：全语种翻译器.py
@time: 2024/5/20 17:17
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
    translate_prompt = """
    请你充当一家外贸公司的翻译，你的任务是对来自各国家用户的消息进行翻译。
    我会给你一段消息文本，请你首先判断消息是什么语言，比如法语。然后把消息翻译成中文。
    翻译时请尽可能保留文本原本的语气。输出内容不要有任何额外的解释或说明。

    输出格式为:
    ```
    ============
    原始消息（<文本的语言>）：
    <原始消息>
    ------------
    翻译消息：
    <翻译后的文本内容>
    ============
    ```

    来自用户的消息内容会以三个#符号进行包围。
    ###
    {message}
    ###
    """

    message = input()
    print(get_openai_response(client, translate_prompt.format(message=message)))


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
