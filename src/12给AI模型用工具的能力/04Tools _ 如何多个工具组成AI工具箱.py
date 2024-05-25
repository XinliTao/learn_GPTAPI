#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 04Tools _ 如何多个工具组成AI工具箱.py
@time: 2024/5/24 11:15
@software: PyCharm
"""
from langchain import hub
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool, Tool
from langchain_experimental.agents.agent_toolkits import create_csv_agent, create_python_agent
from langchain_experimental.tools import PythonREPLTool
from langchain_openai import ChatOpenAI

from src.utils import get_api


class TextLengthTool(BaseTool):
    name = "文本字数计算工具"
    description = "当你需要计算文本包含的字数时，使用此工具"

    def _run(self, text):
        return len(text)


def main(api_key, base_url):
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key, openai_api_base=base_url)
    """定义对应的执行器"""
    python_agent_executor = create_python_agent(
        llm=model,
        tool=PythonREPLTool(),
        verbose=True,
        agent_executor_kwargs={"handle_parsing_errors": True}
    )
    csv_agent_executor = create_csv_agent(
        llm=model,
        path="src/12给AI模型用工具的能力/house_price.csv",
        verbose=True,
        agent_executor_kwargs={"handle_parsing_errors": True}
    )
    tools = [
        # 调用tolls模块下的Tool方法，name参数为给工具起的名字，description赋值为给工具的描述，func参数需要赋值为使用工具时调用的函数或方法
        Tool(
            name="Python代码工具",
            description="""当你需要借助Python解释器时，使用这个工具。
            用自然语言把要求给这个工具，它会生成Python代码并返回代码执行的结果。""",
            func=python_agent_executor.invoke
        ),
        Tool(
            name="CSV分析工具",
            description="""当你需要回答有关house_price.csv文件的问题时，使用这个工具。
            它接受完整的问题作为输入，在使用Pandas库计算后，返回答案。""",
            func=csv_agent_executor.invoke
        ),
        TextLengthTool()  # 继承了BaseTool数据类型属于工具，不需要额外做其他步骤
    ]

    # 常见记忆实例
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )

    prompt = hub.pull("hwchase17/structured-chat-agent")
    print(prompt)
    agent = create_structured_chat_agent(
        llm=model,
        tools=tools,
        prompt=prompt
    )
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )
    # 提问相关问题
    agent_executor.invoke({"input": "第8个斐波那契数列的数字是多少？"})
    agent_executor.invoke({"input": "house_price数据集里，所有房子的价格平均值是多少？用中文回答"})
    agent_executor.invoke({"input": "'君不见黄河之水天上来奔流到海不复回'，这句话的字数是多少？"})


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
