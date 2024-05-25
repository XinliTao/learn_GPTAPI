#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: utils.py
@time: 2024/5/21 15:33
@software: PyCharm
"""
from langchain.prompts import ChatPromptTemplate
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI
# from src.utils import get_api


def generate_script(subject, video_length, creativity, api_key, base_url):
    """创建提示模板"""
    title_template = ChatPromptTemplate.from_messages([
        ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题，中文回答")
    ])
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本语言为中文，脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")
        ]
    )

    """定义模型"""
    model = ChatOpenAI(openai_api_key=api_key, openai_api_base=base_url, temperature=creativity)
    # 标题链
    title_chain = title_template | model
    # 脚本链
    script_chain = script_template | model

    """获取结果"""
    # 标题
    title = title_chain.invoke({"subject": subject}).content
    # 脚本
    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)
    script = script_chain.invoke({"title": title, "duration": video_length, "wikipedia_search": search_result}).content

    return search_result, title, script


if __name__ == '__main__':
    wikipedia_result, ai_title, ai_script = generate_script("sora模型", 1, 0.7, **get_api("course_giveaway"))
    print("维基百科搜索结果为：\n", wikipedia_result)
    print("AI生成标题为：\n", ai_title)
    print("AI生成脚本为：\n", ai_script)
