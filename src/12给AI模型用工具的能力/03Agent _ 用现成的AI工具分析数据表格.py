#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 03Agent _ 用现成的AI工具分析数据表格.py
@time: 2024/5/24 11:03
@software: PyCharm
"""
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI

from src.utils import get_api


def main(api_key, base_url):
    """PythonREPLTool表示python交互式解释器，可以用于执行python命令"""
    agent_executor = create_csv_agent(
        llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key, openai_api_base=base_url),
        path="src/12给AI模型用工具的能力/house_price.csv",
        verbose=True,
        # create_python_agent不直接支持handle_parsing_errors参数，但agent_executor_kwargs可赋值为一个表示更多参数的字典
        agent_executor_kwargs={"handle_parsing_errors": True}
    )
    # 传入与csv数据集相关的问题
    agent_executor.invoke({"input": "数据集有多少行？用中文回复"})
    agent_executor.invoke({"input": "数据集包含哪些变量？用中文回复"})
    agent_executor.invoke({"input": "数据集里，所有房子的价格平均值是多少？用中文回复"})
    agent_executor.invoke({"input": "数据集里，所有房子的装修状态包含哪些种类？你认为它们具体表示什么意思？用中文回复"})


if __name__ == '__main__':
    """csv是一种非常常见的用于存储数据的纯文本格式，全称是Comma-Separated Values"""
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
