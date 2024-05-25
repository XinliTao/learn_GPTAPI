#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 02Prompt Template _ 让模型的输入更灵活.py
@time: 2024/5/21 12:08
@software: PyCharm
"""
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import SystemMessagePromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate, \
    ChatPromptTemplate
from src.utils import get_api


def part_prompt(model, input_variables):
    system_template_text = "你是一位专业的翻译，能够将{input_language}翻译成{output_language}，并且输出文本会根据用户要求的任何语言风格进行调整。请只输出翻译后的文本，不要有任何其它内容。"
    system_prompt_template = SystemMessagePromptTemplate.from_template(system_template_text)
    print("system_prompt_template需要的参数：", system_prompt_template.input_variables)

    human_template_text = "文本：{text}\n语言风格：{style}"
    human_prompt_template = HumanMessagePromptTemplate.from_template(human_template_text)
    print("human_prompt_template需要的参数：", human_prompt_template.input_variables)

    """单条信息"""
    system_prompt = system_prompt_template.format(input_language="英语", output_language="汉语")
    human_prompt = human_prompt_template.format(text="I'm so hungry I could eat a horse", style="文言文")
    response = model.invoke([
        system_prompt,
        human_prompt
    ])
    print("单条信息：", response.content)

    """for循环进行迭代"""
    for item in input_variables:
        response = model.invoke([
            system_prompt_template.format(input_language=item["input_language"],
                                          output_language=item["output_language"]),
            human_prompt_template.format(text=item["text"], style=item["style"])])
        print("for循环迭代：", response.content)


def combine_prompt(model, input_variables):
    """单条信息"""
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system",
             "你是一位专业的翻译，能够将{input_language}翻译成{output_language}，并且输出文本会根据用户要求的任何语言风格进行调整。请只输出翻译后的文本，不要有任何其它内容。"),
            ("human", "文本：{text}\n语言风格：{style}"),
        ]
    )
    print("prompt_template需要的参数：", prompt_template.input_variables)

    prompt_value = prompt_template.invoke({"input_language": "英语", "output_language": "汉语",
                                           "text": "I'm so hungry I could eat a horse", "style": "文言文"})
    print("prompt_value的对象类型为ChatPromptValue，消息列表为：", prompt_value.messages)

    response = model.invoke(prompt_value)
    print("单条信息：", response.content)

    """for循环进行迭代"""
    for item in input_variables:
        response = model.invoke(prompt_template.invoke(
            {"input_language": item["input_language"], "output_language": item["output_language"],
             "text": item["text"], "style": item["style"]}))
        print("for循环迭代：", response.content)


def main(api_key, base_url):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)
    input_variables = [
        {
            "input_language": "英语",
            "output_language": "汉语",
            "text": "I'm so hungry I could eat a horse",
            "style": "文言文"
        },
        {
            "input_language": "法语",
            "output_language": "英语",
            "text": "Je suis désolé pour ce que tu as fait",
            "style": "古英语"
        },
        {
            "input_language": "俄语",
            "output_language": "意大利语",
            "text": "Сегодня отличная погода",
            "style": "网络用语"
        },
        {
            "input_language": "韩语",
            "output_language": "日语",
            "text": "너 정말 짜증나",
            "style": "口语"
        }
    ]
    print("*******************part_prompt*******************")
    part_prompt(model, input_variables)
    print("*******************combine_prompt*******************")
    combine_prompt(model, input_variables)


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
