#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
权重计算
@author: zhengxiaoyao0716
"""

from numpy import mat, pad, nan

from mmp import calc
from data import read_data


def main():
    """Entrypoint"""
    dataset = read_data('input.weight.txt')
    tasks = [calc([(data[i], data[i + 1])
                   for i in range(0, len(data), 2)]) for data in dataset]
    width = max(len(x) for x, _ in tasks)
    collect = [pad(x, (0, width - len(x)), mode='constant', constant_values=nan)
               for x, _ in tasks]
    print('')
    print('Output:')
    print(mat(collect))


if __name__ == '__main__':
    main()
