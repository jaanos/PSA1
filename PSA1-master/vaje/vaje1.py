# -*- coding: utf-8 -*-
# Algoritmi s prvih vaj

def fib1(n):
    """Rekurzivni Fibonacci"""
    if n == 0:
        return 0
    elif n == 1:
        return 1:
    else:
        return fib1(n-2) + fib1(n-1)

def fib2(n):
    """Iterativni Fibonacci"""
    a, b = 0, 1
    if n == 0:
        return a
    while n > 1:
        a, b = b, a+b
        n -= 1
    return b

def mul(x, y):
    """Rekurzivno množenje po bitih"""
    if y == 0:
        return 0
    if y % 2 == 0:
        return mul(x, y//2) << 1
    else:
        return x + (mul(x, y//2) << 1)

def modpow(x, y, n):
    """Potenciranje po modulu z metodo kvadriraj in množi"""
    z = 1
    while y != 0:
        if y % 2 == 1:
            z = z*x % n
        x = x*x % n
        y = y // 2
    return z
