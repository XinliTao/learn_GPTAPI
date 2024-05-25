#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 06Chain _ 串起提示模板-模型-输出解析器.py
@time: 2024/5/21 13:54
@software: PyCharm
"""
from src.utils import get_api
# 帮助构建输入的聊天提示模板
from langchain.prompts import ChatPromptTemplate
# 聊天模型
from langchain_openai import ChatOpenAI
# 帮助解析输出的输出解析器
from langchain.output_parsers import CommaSeparatedListOutputParser

"""
以上都实现了LangChain的Runnable接口，都具有invoke方法：
    1.Dictionary字典 => Prompt Template提示模板 => Prompt Value提示值
    2.Prompt Value提示值 || List of Chat Messages聊天消息列表 => Chat Model聊天模型 => Chat Message聊天信息
    3.Chat Message => Output Parser输出解析器 => 解析结果（类型取决于解析器）
"""


def main(api_key, base_url):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "{parser_instructions}"),
        ("human", "列出5个{subject}色系的十六进制颜色码。")
    ])

    output_parser = CommaSeparatedListOutputParser()
    parser_instructions = output_parser.get_format_instructions()

    """层层调用invoke方法"""
    result = output_parser.invoke(
        model.invoke(
            prompt.invoke(
                {"subject": "莫兰迪", "parser_instructions": parser_instructions}
            )
        )
    )
    print("层层调用invoke方法：", result)

    """管道操作；组件之间的上下游关系清晰明了"""
    chat_model_chain = prompt | model | output_parser  # 这种写法叫做LangChain表达式语言，简称LCEL。多个组件的一次性调用叫做Chain（链）
    result = chat_model_chain.invoke({"subject": "莫兰迪", "parser_instructions": parser_instructions})
    print("管道操作：", result)


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
