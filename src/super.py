#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
超极限矩阵
@author: zhengxiaoyao0716
"""

from numpy import mat, e, max, inf, isinf

from data import read_data


def row_diff(row):
    """Calculate the diff of row"""
    return max([abs(col - row[0]) if not isinf(col) else inf for col in row])


def main():
    """Entrypoint"""
    raw = mat(read_data('input.super.txt'))
    count, diff = 0, 1
    data = raw
    while count < 100 and diff > 0.5 * (10 ** -4):
        new = data * raw
        count += 1
        diff = max([row_diff([col for col in row if col != 0])
                    for row in new.tolist()])  # pylint: disable=E1101
        if isinf(diff):
            break
        data = new
    print(data)


if __name__ == '__main__':
    main()
