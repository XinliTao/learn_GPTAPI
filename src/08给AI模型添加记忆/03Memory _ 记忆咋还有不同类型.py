#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: 03Memory _ 记忆咋还有不同类型.py
@time: 2024/5/22 15:59
@software: PyCharm
"""
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.memory import (ConversationBufferMemory, ConversationBufferWindowMemory,
                              ConversationSummaryMemory, ConversationSummaryBufferMemory, ConversationTokenBufferMemory)

from src.utils import get_api


def type_conversation_buffer_memory(model):
    """
    ConversationBufferMemory
        一字不漏地存储对话的所有消息，不存在任何信息遗漏，存储过程简单直接
        随着对话轮数的增加，传给模型的历史消息列表越来越长，消耗的token越来越多，
        并且消息长度一旦达到模型上下文窗口的token上限，就没法直接传给模型了，需要手动进行截断容纳进窗口里
    """
    memory = ConversationBufferMemory(return_messages=True)
    chain = ConversationChain(llm=model, memory=memory)
    res = chain.invoke({"input": "你好，我的名字是粒粒"})
    print(res, res['input'], res['response'], sep="\n")
    res = chain.invoke({"input": "我的名字是什么？"})
    print(res, res['input'], res['response'], sep="\n")


def type_conversation_buffer_window_memory(model):
    """
    ConversationBufferWindowMemory
        允许指定k参数为一个数字，表示窗口的尺寸，即记忆里最多会存储的历史【对话】数量
        如果k值把握地好，对话可以一直进行下去，无需担心记忆里存储的对话太多，挤爆上下文窗口
        但相应的问题在于，最多只有k轮消息会被存储，对话轮数超过时，前面的信息就直接丢失了
    """
    memory = ConversationBufferWindowMemory(k=1, return_messages=True)
    chain = ConversationChain(llm=model, memory=memory)
    chain.invoke({"input": "你好，我的名字是粒粒"})
    res = chain.invoke({"input": "我是一个程序员"})
    print(res, res['input'], res['response'], sep="\n")
    res = chain.invoke({"input": "我的名字是什么？"})
    print(res, res['input'], res['response'], sep="\n")


def type_conversation_summary_memory(model):
    """
    ConversationSummaryMemory
        为了控制存储内容的长度，又不直接丢弃之前的对话。
        不是直接储存原始的历史消息，而是对之前的对话内容先进行总结，然后储存总结，可以更晚达到上下文窗口上限
        总结也是由大模型做的，创建ConversationChain时需要传入LLM，总结过程需要消耗token，且可能会丢失一些细节
        当对话轮数不多时，可能总结都比原始消息长，随着轮数增加，总结内容变得比原始对话更精练
    """
    memory = ConversationSummaryMemory(return_messages=True, llm=model)
    chain = ConversationChain(llm=model, memory=memory)
    chain.invoke({"input": "你好，我的名字是粒粒"})
    res = chain.invoke({"input": "我是一个程序员，你呢？"})
    print(res, res['input'], res['response'], sep="\n")
    res = chain.invoke({"input": "我的名字是什么？"})
    print(res, res['input'], res['response'], sep="\n")


def type_conversation_summary_buffer_memory(model):
    """
    ConversationSummaryBufferMemory
        max_token_limit指定token数量上限，储存消息比较少的时候，原封不动储存，类似ConversationBufferMemory
        当储存消息变多，达到token上限后，开始进行总结，类似ConversationSummaryMemory，不同之处在于，不是总结所有信息，从更久远的信息开始总结
        没有超过token上限的那些更近的消息，仍然储存原始内容，记得更多细节，但是总结任务仍然需要消耗额外的token
    """
    memory = ConversationSummaryBufferMemory(llm=model, max_token_limit=100, return_messages=True)
    chain = ConversationChain(llm=model, memory=memory)
    chain.invoke({"input": "你好，我的名字是粒粒"})
    res = chain.invoke({"input": "我是一个程序员，你呢？"})
    print(res, res['input'], res['response'], sep="\n")
    res = chain.invoke({"input": "我的名字是什么？我前面说过的"})
    print(res, res['input'], res['response'], sep="\n")


def type_conversation_token_buffer_memory(model):
    """
    ConversationTokenBufferMemory
        与ConversationBufferWindowMemory相似，都是直接储存原始消息。
        达到某个上限（已储存消息的token数）后，只保留没有超过上限的部分。
        由于当前LLM都有明确的上下文窗口，并且窗口长度是以token为单位计算的，所以这也是一个很实用的记忆
    """
    memory = ConversationTokenBufferMemory(llm=model, max_token_limit=200, return_messages=True)
    chain = ConversationChain(llm=model, memory=memory)
    chain.invoke({"input": "你好，我的名字是粒粒"})
    res = chain.invoke({"input": "我是一个程序员，你呢？"})
    print(res, res['input'], res['response'], sep="\n")
    res = chain.invoke({"input": "我的名字是什么？我前面说过的"})
    print(res, res['input'], res['response'], sep="\n")


def main(api_key, base_url):
    """五种不同的记忆各有优劣势，可以根据需求，用在不同的场景下"""
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key, openai_api_base=base_url)
    print("******************ConversationBufferMemory******************")
    type_conversation_buffer_memory(model)
    print("******************ConversationBufferWindowMemory******************")
    type_conversation_buffer_window_memory(model)
    print("******************ConversationSummaryMemory******************")
    type_conversation_summary_memory(model)
    print("******************ConversationSummaryBufferMemory******************")
    type_conversation_summary_buffer_memory(model)
    print("******************ConversationTokenBufferMemory******************")
    type_conversation_token_buffer_memory(model)


if __name__ == '__main__':
    main(**get_api('course_giveaway'))
    # main(**get_api('my_own'))
