# -*- coding: utf-8 -*-

"""
计算mmp问题
"""

from numpy import mat, ones
from openopt.oo import MMP


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


def calc(kbs, t=1):
    """Entrypoint"""
    n = var_num(len(kbs) / 2)

    """
    t = max(min(
        t - ((k1 - 1)w1 + b1w2),
        t - ((k2 - 1)w1 + b2w3),
        t - ((k3 - 1)w2 + b3w3),
        t - (k4w1 + (b4 - 1)w2),
        t - (k5w1 + (b5 - 1)w3),
        t - (k6w2 + (b6 - 1)w3),
    )) = -min(max(-Fi))
    """
    Fx = []
    fx = lambda kl, l, kr, r: lambda x: -(t - (kl * x[l] + kr * x[r]))
    xi = gen_xi(n)
    Fx += [fx(k - 1, xi.next(), b, xi.next()) for k, b in kbs[:len(kbs) / 2]]
    xi = gen_xi(n)
    Fx += [fx(k, xi.next(), b - 1, xi.next()) for k, b in kbs[len(kbs) / 2:]]

    """
    0 <= wi <= 1
    """
    lb = [0] * n
    ub = [1] * n

    """
    [1, ..., 1]*w = 1
    """
    Aeq = mat(ones(n))
    beq = 1

    """
    initial value
    """
    x0 = list(range(n))

    p = MMP(Fx, x0,
            lb=lb, ub=ub, Aeq=Aeq, beq=beq, xtol=1e-6, ftol=1e-6)
    r = p.solve('nsmm', iprint=1, maxIter=1e3, minIter=1e2)
    print(r.xf, r.ff)
    return r.xf, -r.ff
