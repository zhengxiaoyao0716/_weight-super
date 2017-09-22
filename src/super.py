#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
超极限矩阵
@author: zhengxiaoyao0716
"""

from numpy import mat, e, max

from data import read_data


def main():
    """Entrypoint"""
    data = mat(read_data('input.super.txt'))
    diff = 1
    count = 0
    while count < 100 or diff > e**-100:
        count += 1
        new = data * data
        diff = max(new - data)
        data = new
    print(data)


if __name__ == '__main__':
    main()
