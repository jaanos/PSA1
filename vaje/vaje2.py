# -*- coding: utf-8 -*-
# Algoritmi z drugih vaj

def euclid(m, n):
    """Evklidov algoritem"""
    while n != 0:
        m, n = n, m % n
    return m

def exteuclid(m, n):
    """
    Razširjeni Evklidov algoritem.

    Vrača (g, a, b), kjer je g = gcd(m, n) in g = a*m + b*n.
    Če je g = 1, velja a mod n = m^-1 mod n in b mod m = n^-1 mod m.
    """
    p, q, r, s = 1, 0, 0, 1
    while n != 0:
        k = m//n
        m, n = n, m - k*n
        p, q = q, p - k*q
        r, s = s, r - k*s
    return (m, p, r)

def karatsuba(m, n, b):
    """Množenje z metodo deli in vladaj"""
    if b == 0:
        return m*n
    m1, m2 = m >> b, m & ~(-1 << b)
    n1, n2 = n >> b, n & ~(-1 << b)
    mn1 = karatsuba(m1, n1, b//2)
    mn2 = karatsuba(m2, n2, b//2)
    mn0 = karatsuba(m1+m2, n1+n2, b//2) - mn1 - mn2
    return (mn1 << 2*b) + (mn0 << b) + mn2
