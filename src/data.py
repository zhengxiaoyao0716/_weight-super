#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
数据处理
"""


def read_data(path):
    """Read data"""
    with open(path) as f:
        return [[float(word) for word in line.split()] for line in f.readlines() if line != '\n']
