# -*- coding: utf-8 -*-

def strnjenoPodzaporedje(a):
    n = len(a)
    s = [(0, 0)]
    for i in range(n):
        t, z = max(s[i], (0, i))
        s.append((t + a[i], z))
    return max((v, z, k) for k, (v, z) in enumerate(s))

def optimalnaPot(a, m):
    assert a[0] == 0
    n = len(a)
    s = [(0, None)]
    for i in range(n-1):
        s.append(min((s[j][0] + (m-a[i+1]+a[j])**2, j) for j in range(i+1)))
    pot = []
    x = n-1
    while x is not None:
        pot.append(x)
        x = s[x][1]
    return (s[-1][0], list(reversed(pot)))

def besede(s, beseda):
    n = len(s)
    d = [0]
    for i in range(n):
        try:
            d.append(next(j for j in reversed(range(i+1))
                          if d[j] is not None and beseda(s[j:i+1])))
        except StopIteration:
            d.append(None)
    if d[-1] is None:
        return False
    b = []
    i = n
    while i > 0:
        b.append(s[d[i]:i])
        i = d[i]
    return list(reversed(b))
