# -*- coding: utf-8 -*-
from vaje3 import Queue

def queueMerge(l):
    """
    Iterativna različica mergesort-a.

    Uporablja vrsto (razred Queue) iz modula vaje3.
    """
    if len(l) == 0:
        return l
    q = Queue()
    for x in l:
        q.enqueue([x])
    while len(q) > 1:
        a = q.dequeue()
        b = q.dequeue()
        i, j = 0, 0
        c = []
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                c.append(a[i])
                i += 1
            else:
                c.append(b[j])
                j += 1
        c += a[i:] + b[j:]
        q.enqueue(c)
    return q.dequeue()

def select(l, k):
    """
    Iskanje k-tega najmanjšega elementa v seznamu l.

    Algoritem porabi O(1) dodatnega prostora
    in najde k-ti element v pričakovanem času O(log n).
    Pri tem lahko preuredi elemente v seznamu l.
    """
    a, b = 0, len(l) - 1
    assert a <= k and k <= b
    while a < b:
        pivot = l[k]
        i, j = a, b
        while i < j:
            while l[i] < pivot:
                i += 1
            while l[j] > pivot:
                j -= 1
            if i <= j:
                l[i], l[j] = l[j], l[i]
                i += 1
                j -= 1
        if k < i:
            b = i-1
        if k > j:
            a = j+1
    return l[k]

def find(x, get):
    """
    Bisekcija na urejenem seznamu neznane dolžine.

    Poišče indeks elementa x v seznamu neznane dolžine,
    do katerega lahko dostopamo s pomočjo funkcije get.
    Algoritem teče v času O(log n),
    kjer je n dejanska dolžina seznama.

    V primerjavi z algoritmom z vaj je tukaj spremenjena prva zanka,
    ki premika tudi levo krajišče intervala in se ustavi,
    če najde interval, ki lahko vsebuje iskani element.
    """
    a, b = 0, 1
    z = get(b)
    while z is not None:
        if x < z:
            b -= 1
            break
        elif x == z:
            return b
        else:
            a, b = b + 1, 2 * b
            z = get(b)
    while a < b:
        c = (a + b) // 2
        z = get(c)
        if z is None or x < z:
            b = c - 1
        elif x == z:
            return c
        else:
            a = c + 1
    if x == get(a):
        return a
    else:
        return None

def bucketSort(l):
    """
    Urejanje seznama celih števil v času O(n + M),
    kjer je M razlika med največjim in najmanjšim elementom seznama.
    """
    a = min(l)
    b = max(l)
    M = b - a + 1
    c = [0] * M
    for x in l:
        c[x - a] += 1
    s = []
    for i in range(M):
        s += [i + a] * c[i]
    return s
