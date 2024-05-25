#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: utils.py
@time: 2024/5/21 17:23
@software: PyCharm
"""
from prompt_template import system_template_text, user_template_text
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from xiaohongshu_model import Xiaohongshu
# from src.utils import get_api


def generate_xiaohongshu(theme, api_key, base_url):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template_text),
        ("user", user_template_text)
    ])
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)
    output_parser = PydanticOutputParser(pydantic_object=Xiaohongshu)
    chain = prompt | model | output_parser
    result = chain.invoke({
        "parser_instructions": output_parser.get_format_instructions(),
        "theme": theme
    })
    return result


if __name__ == '__main__':
    print(generate_xiaohongshu("大模型", **get_api("course_giveaway")))
