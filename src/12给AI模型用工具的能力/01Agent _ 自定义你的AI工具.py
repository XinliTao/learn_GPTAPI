#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 01Agent _ 自定义你的AI工具.py
@time: 2024/5/23 21:26
@software: PyCharm
"""
# LangChain Hub是一个用于管理和共享LangChain相关资源的在线平台，从中可以获得用户上传的各种目的提示词
from langchain import hub
# agent经过多个步骤来产生输出，每个步骤都会遵循推理、行动、观察框架
from langchain.agents import create_structured_chat_agent, AgentExecutor, BaseSingleActionAgent
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI

from src.utils import get_api


class TextLengthTool(BaseTool):
    """
    自定义一个类工具
        1.模型在计算文本长度的生活，本质上是在预测下一个token，是在猜答案
        2.为了帮助模型理解工具的作用，需要定义两个类变量name和description
    """
    # 定义类变量
    name = "文本字数计算工具"
    description = "当你被要求计算文本的字数时，使用此工具"

    def _run(self, text):
        # 实现对应功能
        return len(text)


def main(api_key, base_url):
    # 定义模型，并且设置低的创造率
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=api_key, openai_api_base=base_url)

    # 当模型还没有使用我们自定义的工具
    res = model.invoke([HumanMessage(content="'君不见黄河之水天上来奔流到海不复回'，这句话的字数是多少？")])
    print("未使用自定义工具：", res.content)

    # tolls列表表示agent列表可以使用到的所有工具
    tools = [TextLengthTool()]

    # 传入我们要拉取的提示词在LangChain Hub上的路径，从而获取提示模板ChatPromptTemplate，其中把工具介绍作为变量，留给我们后续插入相关信息
    prompt = hub.pull("hwchase17/structured-chat-agent")
    print("ChatPromptTemplate：\n", prompt)

    # 初始化agent，实际执行的是agent_executor
    agent = create_structured_chat_agent(
        llm=model,
        tools=tools,
        prompt=prompt
    )
    # 定义记忆类型
    memory = ConversationBufferMemory(
        memory_key='chat_history',  # 之前传入的提示模板里，对应记忆的变量名叫做chat_history
        return_messages=True
    )
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,  # 总所周知，程序员不看警告
        tools=tools,
        memory=memory,
        # 模型如果没有按ReAct框架输出，会出现解析错误，程序默认直接中止。为true表示把错误作为观察发送回大模型，让大模型自行推理处理错误。
        handle_parsing_errors=True,
        # 是否以详细模式运行，默认为false，想了解agent行动过程，打印出日志文件，就设为true
        verbose=True
    )
    res = agent_executor.invoke({"input": "'君不见黄河之水天上来奔流到海不复回'，这句话的字数是多少？"})
    print("使用自定义工具：", res)
    res = agent_executor.invoke({"input": "请你充当我的物理老师，告诉我什么是量子力学"})
    print("提问和字数不相关的问题：", res)


if __name__ == '__main__':
    """
    agent通过集成适应不同需求、解决不同问题的工具以及复杂的决策和推理过程能更好地理解用户需求，处理复杂的问题，让我们有机会创造出更智能和强大的AI助手
    """
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
