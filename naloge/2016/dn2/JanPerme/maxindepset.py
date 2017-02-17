# -*- coding: utf-8 -*-
import operator
def maxCycleTreeIndependentSet(T, w):
    """
    Najtežja neodvisna množica
    v kartezičnem produktu cikla C_k in drevesa T z n vozlišči,
    kjer ima tabela tež w dimenzije k×n (k >= 2).

    Vrne par (c, s), kjer je c teža najdene neodvisne množice,
    s pa je seznam vozlišč v neodvisni množici,
    torej seznam parov oblike (i, u) (0 <= i <= k-1, 0 <= u <= n-1).
    """
    n = len(T)
    assert all(len(r) == n for r in w), \
        "Dimenzije tabele tež ne ustrezajo številu vozlišč v drevesu!"
    assert all(all(u in T[v] for v in a) for u, a in enumerate(T)), \
        "Podani graf ni neusmerjen!"
    k = len(w)
    slovar=dict()
    slovar2=dict()
    assert k >= 2, "k mora biti vsaj 2!"
    if n == 0:
        return (0, [])
    def drevo(T,w,V,vozlisce,obiskani):
        obiskani1=obiskani.copy()
        obiskani1.append(vozlisce)
        mozni_sosedi=[]
        for sosed in T[vozlisce]:
            if sosed not in obiskani1:
                mozni_sosedi.append(sosed)
        cikel=[i for i in range(k)]
        for v in V:
            del cikel[cikel.index(v)]
        H=memorizacija2(cikel)
        maxmnozica, maximum = max(enumerate(sum(w[element][vozlisce] for element in M)+sum(memorizacija1(M,sosed,obiskani1)[0] for sosed in mozni_sosedi) for M in H), key=operator.itemgetter(1))
        izbrani=mnozica(H[maxmnozica],vozlisce)
        for sosed in mozni_sosedi:
            izbrani+=memorizacija1(H[maxmnozica],sosed,obiskani1)[1]
        return [maximum,izbrani]
    def neodvisna_mn(A):
        if len(A)!=0:
            mnozica=[[A[0]]]
            for j in range(1,len(A)):
                pmn=[]
                for M in mnozica:
                    if A[j]==0 and (1 in M or k-1 in M): pass
                    elif A[j]==(k-1) and (0 in M or k-2 in M):pass
                    elif (A[j]+1) in M or (A[j]-1) in M: pass
                    else:
                        element=M.copy()
                        pmn+=[element+[A[j]]]
                mnozica+=pmn
            mnozica+=memorizacija2(A[1:])
            return mnozica
        else:
            return [[]]
    def mnozica(G,vozlisce):
        A=[]
        for a in G:
            A.append((a,vozlisce))
        return A
    def memorizacija1(V,sosed,obiskani1):
        A=frozenset(V)
        B=frozenset(obiskani1)
        index=(A,sosed,B)
        if index in slovar:
            return slovar[index]
        else:
            slovar[index]=drevo(T,w,V,sosed,obiskani1)
            return slovar[index]
    def memorizacija2(A):
        B=frozenset(A)
        if B in slovar2:
            return slovar2[B]
        else:
            slovar2[B]=neodvisna_mn(A)
            return slovar2[B]
    return drevo(T,w,[],T[0][0],[])
    
