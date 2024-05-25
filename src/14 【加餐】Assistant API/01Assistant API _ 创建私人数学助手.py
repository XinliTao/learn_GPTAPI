#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 01Assistant API _ 创建私人数学助手.py
@time: 2024/5/25 0:06
@software: PyCharm
"""
from openai import OpenAI

from src.utils import get_api


def main(api_key, base_url):
    # 获取客户端实例
    client = OpenAI(api_key=api_key, base_url=base_url)

    # 定义一个助手
    assistant = client.beta.assistants.create(
        model="gpt-3.5-turbo",
        name="数学助手",
        instructions="你是一个数学助手，可以通过编写和运行代码来回答数学相关问题。",
        # 列表里的每一个元素都代表AI可以使用的工具
        tools=[{"type": "code_interpreter"}]
    )

    # 创建线程，不同用户应该有独立的线程，历史对话消息才不会混淆，而且同一个用户也可以有不同的对话线程
    thread = client.beta.threads.create()
    print("线程Id：", thread.id)

    # 创建一条消息
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",  # 助手对应的是字符串assistant
        content="我需要解这个方程`5x^2−1200x+72000=0，未知数应该是多少？"
    )

    # 创建一个运行
    """
        即使没有显式地将消息message传递给运行run，助手还是会处理与该线程相关的所有消息。
        这是因为运行是与特定线程关联的，而该线程中的所有消息（包括新创建的消息）都会被纳入助手的上下文中进行处理。
    """
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="请称呼用户为粒粒",  # 提供一些额外的，仅仅针对此次运行的指令
    )
    # 当这个创建Run的代码开始执行后，我们并不能马上得到来自AI的回复
    print(run)

    # 返回对应的Run实例，里面的status属性值就对应了返回那一刻的状态
    print(client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    ).status)  # queued表示排队中，in_progress表示生成中，completed表示返回成功

    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"运行状态：{keep_retrieving_run.status}")
        if keep_retrieving_run.status == "completed":
            break

    # 获得线程上的所有消息
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages.data)  # 是一个message的列表

    for data in messages.data:
        print(data.content[0].text.value)
        print("------")

    # 以上过程封装为一个函数
    get_response_from_assistant(client, assistant, thread, "2的56次方等于多少")


def get_response_from_assistant(client, assistant, thread, prompt, run_instruction=""):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=run_instruction
    )

    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            break

    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    for data in messages.data:
        print("\n")
        print(data.content[0].text.value)
        print("------")


if __name__ == '__main__':
    # 课程赠送的api无assistant权限
    main(**get_api('course_giveaway'))
