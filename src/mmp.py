# -*- coding: utf-8 -*-

"""
计算mmp问题
"""

from numpy import mat, ones
from openopt.oo import MMP


def calc(k, t=1):
    """Entrypoint"""
    """
    t = max(min(
        t - ((k0 - 1)w1 + k0w2),
        t - ((k1 - 1)w1 + k1w3),
        t - ((k2 - 1)w2 + k2w3),
        t - (k3w1 + (k3 - 1)w2),
        t - (k4w1 + (k4 - 1)w3),
        t - (k5w2 + (k5 - 1)w3),
    )) = -min(max(-Fi))
    """
    Fx = [
        lambda x: -(t - ((k[0] - 1) * x[0] + k[0] * x[1])),
        lambda x: -(t - ((k[1] - 1) * x[0] + k[1] * x[2])),
        lambda x: -(t - ((k[2] - 1) * x[1] + k[2] * x[2])),
        lambda x: -(t - (k[3] * x[0] + (k[3] - 1) * x[1])),
        lambda x: -(t - (k[4] * x[0] + (k[4] - 1) * x[2])),
        lambda x: -(t - (k[5] * x[1] + (k[5] - 1) * x[2])),
    ]
    """
    0 <= w <= 1
    """
    lb = [0] * 3
    ub = [1] * 3
    """
    [1, 1, 1]*w = 1
    """
    Aeq = mat(ones(3))
    beq = 1

    x0 = [0, 1, 2]

    p = MMP(Fx, x0,
            lb=lb, ub=ub, Aeq=Aeq, beq=beq, xtol=1e-6, ftol=1e-6)
    r = p.solve('nsmm', iprint=-1, maxIter=1e3, minIter=1e2)
    # print(r.xf, r.ff)
    return r.xf, -r.ff
