#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
权重计算
@author: zhengxiaoyao0716
"""

from numpy import mat

from mmp import calc
from data import read_data


def main():
    """Entrypoint"""
    dataset = read_data('input.weight.txt')
    tasks = [calc(data) for data in dataset]
    collect = [x for x, _ in tasks]
    print(mat(collect))


if __name__ == '__main__':
    main()
