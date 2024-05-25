#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 05OutputParser_从模型输出里提取JSON.py
@time: 2024/5/21 13:08
@software: PyCharm
"""
from typing import List
# PydanticOutputParser 指挥AI输出符合格式要求的JSON，并且帮我们进行解析
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
# BaseModel用于创建数据模式，Field定义字段属性，提供额外信息和验证条件
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from src.utils import get_api


class BookInfo(BaseModel):
    book_name: str = Field(description="书籍的名字", example="百年孤独")
    author_name: str = Field(description="书籍的作者", example="加西亚·马尔克斯")
    genres: List[str] = Field(description="书籍的体裁", example=["小说", "文学"])


def main(api_key, base_url):
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)
    """
        OutputParser：
            1.指令里要求模型按照指定的格式输出
            2.解析模型的输出，提取所需的信息
        PydanticOutputParser：
            1.指令里要求模型根据各个字段要求输出JSON
            2.把模型输出的JSON，解析成对应的BookInfo实例
    """
    output_parser = PydanticOutputParser(pydantic_object=BookInfo)
    print("OutputParser指令：\n", output_parser.get_format_instructions())

    # ChatPromptTemplate构造消息提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{parser_instructions} 你输出的结果请使用中文。"),
        ("human", "请你帮我从书籍概述中，提取书名、作者，以及书籍的体裁。书籍概述会被三个#符号包围。\n###{book_introduction}###")
    ])

    # 给提示模板参数传参
    book_introduction = """《明朝那些事儿》，作者是当年明月。2006年3月在天涯社区首次发表，2009年3月21日连载完毕，边写作边集结成书出版发行，一共7本。
    《明朝那些事儿》主要讲述的是从1344年到1644年这三百年间关于明朝的一些故事。以史料为基础，以年代和具体人物为主线，并加入了小说的笔法，语言幽默风趣。对明朝十六帝和其他王公权贵和小人物的命运进行全景展示，尤其对官场政治、战争、帝王心术着墨最多，并加入对当时政治经济制度、人伦道德的演义。
    它以一种网络语言向读者娓娓道出三百多年关于明朝的历史故事、人物。其中原本在历史中陌生、模糊的历史人物在书中一个个变得鲜活起来。《明朝那些事儿》为读者解读历史中的另一面，让历史变成一部活生生的生活故事。
    """
    final_prompt = prompt.invoke({"book_introduction": book_introduction, "parser_instructions": output_parser.get_format_instructions()})

    response = model.invoke(final_prompt)
    print("模型返回结果：\n", response.content)

    result = output_parser.invoke(response)
    print("解析器的invoke方法解析的结果：\n", result)


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
