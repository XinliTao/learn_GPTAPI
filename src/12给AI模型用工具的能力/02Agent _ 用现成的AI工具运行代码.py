#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 02Agent _ 用现成的AI工具运行代码.py
@time: 2024/5/24 1:32
@software: PyCharm
"""
# 导入专门用于创建执行Python代码的agent执行器的函数
from langchain_experimental.agents.agent_toolkits import create_python_agent
# 让AI生成做计算的代码，Program-Aided Language Models（程序复制语言模型，简称PAL）
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI

from src.utils import get_api


def main(api_key, base_url):
    """PythonREPLTool表示python交互式解释器，可以用于执行python命令"""
    agent_executor = create_python_agent(
        llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key, openai_api_base=base_url),
        tool=PythonREPLTool(),
        verbose=True,
        # create_python_agent不直接支持handle_parsing_errors参数，但agent_executor_kwargs可赋值为一个表示更多参数的字典
        agent_executor_kwargs={"handle_parsing_errors": True}
    )
    # 传入与计算相关的问题
    agent_executor.invoke({"input": "7的2.3次方是多少？"})
    agent_executor.invoke({"input": "第12个斐波那契数列的数字是多少？"})


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
