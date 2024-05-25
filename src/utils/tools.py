#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Txl
@file: tools.py
@time: 2024/5/19 22:07
@software: PyCharm
"""
import json


def get_api(key):
    path = "SecretKey.json"
    # 打开并读取 JSON 文件
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data[key]
