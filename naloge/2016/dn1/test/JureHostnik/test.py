# -*- coding: utf-8 -*-
from random import *
from time import *

def rand(nrow, ncol):
    '''
    Vrne seznam dolžine nrow seznamov dolžine ncol
    s celimi števili iz intervala [-10, 10].
    '''
    return [[randint(-10, 10) for j in range(ncol)] for i in range(nrow)]

def cas(left, right):
    '''
    Vrne čas, ki se porabi za produkt left * right.
    '''
    t = clock()
    left * right
    return clock() - t
