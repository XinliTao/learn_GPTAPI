#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 02Assistant API _ 创建文件问答助手.py
@time: 2024/5/25 0:54
@software: PyCharm
"""
from openai import OpenAI

from src.utils import get_api


def main(api_key, base_url):
    # 获取客户端实例
    client = OpenAI(api_key=api_key, base_url=base_url)

    # 得到一个文件对象的实例
    file = client.files.create(
        file=open("src/14 【加餐】Assistant API/论文介绍.pdf", "rb"),
        purpose="assistants"
    )
    # 定义助手
    assistant = client.beta.assistants.create(
        model="gpt-3.5-turbo",
        name="AI论文问答助手",
        instructions="你是一个智能助手，可以访问文件来回答人工智能领域论文的相关问题。",
        tools=[{"type": "retrieval"}],
        file_ids=[file.id]  # 关联文件
    )
    # 创建线程
    thread = client.beta.threads.create()

    get_response_from_assistant(client, assistant, thread, "哪篇论文介绍了Transformer架构？论文链接是什么？")


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
