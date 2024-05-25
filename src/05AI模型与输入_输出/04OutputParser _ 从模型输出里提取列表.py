#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 04OutputParser _ 从模型输出里提取列表.py
@time: 2024/5/21 12:48
@software: PyCharm
"""
# CommaSeparatedListOutputParser 指挥AI输出List，并且帮我们进行解析
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.utils import get_api


def main(api_key, base_url):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)
    """
        OutputParser：
            1.指令里要求模型按照指定的格式输出
            2.解析模型的输出，提取所需的信息
    """
    output_parser = CommaSeparatedListOutputParser()
    # 返回都好分隔列表输出的文字指令
    parser_instructions = output_parser.get_format_instructions()
    print("OutputParser指令：", parser_instructions)

    # ChatPromptTemplate构造消息提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{parser_instructions}"),
        ("human", "列出5个{subject}色系的十六进制颜色码。")
    ])

    # 给提示模板参数传参
    final_prompt = prompt.invoke({"subject": "莫兰迪", "parser_instructions": parser_instructions})
    response = model.invoke(final_prompt)
    print("模型返回结果：", response.content)

    print("解析器的invoke方法解析的结果：", output_parser.invoke(response))


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
