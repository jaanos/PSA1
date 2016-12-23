# -*- coding: utf-8 -*-
__all__ = ['SlowMatrix', 'FastMatrix', 'CheapMatrix']

from ... matrix.JureHostnik.slowmatrix import SlowMatrix
from ... matrix.JureHostnik.fastmatrix import FastMatrix
from ... matrix.JureHostnik.cheapmatrix import CheapMatrix

from random import *
from time import *

def rand(nrow, ncol):
    '''
    Vrne seznam dolžine nrow seznamov dolžine ncol
    s celimi števili iz intervala [-10, 10].
    '''
    return [[randint(-10, 10) for j in range(ncol)] for i in range(nrow)]

def cas(left, right):
    t = clock()
    left * right
    return clock() - t
