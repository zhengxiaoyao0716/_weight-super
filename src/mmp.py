# -*- coding: utf-8 -*-

"""
计算mmp问题
"""

from functools import reduce
from numpy import mat, ones, inf
from scipy.optimize import linprog


def var_num(l):
    """Calculate the num of `w`"""
    i = 1
    n = 1
    while l:
        l -= i
        if l < 0:
            raise 'Illegal length of input'
        n += 1
        i += 1
    return n


def gen_xi(n):
    """generate index of x"""
    l = 0
    r = 0
    while True:
        i = n - 1 - l
        for _ in range(i):
            r += 1
            yield l
            yield r
        l += 1
        r = l


def adjust_kb(kbs, n):
    """adjust kb"""
    # change = lambda a, b: a * b / (a * b + (1 - a) * (1 - b))
    # i = 0
    # for ln in range(n - 1, 0, -1):
    #     for li in range(1, ln):
    #         k, b = kbs[i + ln]
    #         if k != b:
    #             kbs[i + ln] = ()
    #     i += ln
    change = lambda *i: reduce(lambda l, r: l * r, i) ** (float(2) / len(i)) / (
        reduce(lambda l, r: l * r, i) ** (float(2) / len(i)) +
        reduce(lambda l, r: (1 - l) * (1 - r), i) ** (float(2) / len(i))
    )

    def _fn2():
        kbs[1] = kbs[0]

    def _fn3():
        if kbs[1][0] != kbs[1][1] or kbs[4][0] != kbs[4][1]:
            kbs[1] = [change(kbs[0][0], kbs[2][0])] * 2
            kbs[4] = [change(kbs[3][0], kbs[5][0])] * 2

    def _fn4():
        if kbs[4][0] != kbs[4][1] or kbs[10][0] != kbs[10][1]:
            kbs[4] = [change(kbs[3][0], kbs[5][0])] * 2
            kbs[10] = [change(kbs[9][0], kbs[11][0])] * 2
        if kbs[2][0] != kbs[2][1] or kbs[8][0] != kbs[8][1]:
            kbs[2] = [change(kbs[0][0], kbs[3][0], kbs[4][0], kbs[5][0])] * 2
            kbs[8] = [change(kbs[6][0], kbs[9][0], kbs[10][0], kbs[11][0])] * 2
        if kbs[1][0] != kbs[1][1] or kbs[7][0] != kbs[7][1]:
            kbs[1] = [change(kbs[0][0], kbs[2][0])] * 2
            kbs[7] = [change(kbs[6][0], kbs[8][0])] * 2

    [None, None, _fn2, _fn3, _fn4, None, ][n]()
    return kbs


def calc(kbs, t=1):
    """Entrypoint"""
    n = var_num(len(kbs) / 2)

    """
    c^T * x
        z = -t + 0*wi
    """
    c = [-1] + [0] * n

    """
    A_ub * x <= b_ub
        t + ((k1 - 1)w1 + b1w2) <= 1,
        t + ((k2 - 1)w1 + b2w3) <= 1,
        t + ((k3 - 1)w2 + b3w3) <= 1,
        t + (k4w1 + (b4 - 1)w2) <= 1,
        t + (k5w1 + (b5 - 1)w3) <= 1,
        t + (k6w2 + (b6 - 1)w3) <= 1,
    """
    def _a(k, l, b, r):
        a = [1] + [0] * n
        a[l + 1] = k
        a[r + 1] = b
        return a
    A_ub = []
    xi = gen_xi(n)
    A_ub += [_a(k - 1, xi.next(), b, xi.next()) for k, b in kbs[:len(kbs) / 2]]
    xi = gen_xi(n)
    A_ub += [_a(k, xi.next(), b - 1, xi.next()) for k, b in kbs[len(kbs) / 2:]]

    b_ub = [[1,],] * len(kbs)

    """
    A_eq * x == b_eq
        0*t + [1, ..., 1]*w = 1
    """
    A_eq = [[0] + [1] * n]
    b_eq = [1]

    """
    -inf < t < inf, 0 <= wi <= 1
    """
    bounds = ((-inf, inf),) * (n + 1)

    r = linprog(c, A_ub=A_ub, b_ub = b_ub, A_eq = A_eq, b_eq = b_eq, bounds = bounds)
    # print(r)
    print(A_ub)
    print(r.fun, r.x)
    # for k in A_ub:
    #     print(reduce(lambda l, i: l + k[i] * r.x[i], range(n + 1), 0))
    print('')
    return r.x, -r.fun
