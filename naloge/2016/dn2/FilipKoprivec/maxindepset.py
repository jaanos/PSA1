# -*- coding: utf-8 -*-
from typing import Dict
from typing import Tuple, List
from .helpers import generate_bitmasks, make_transitions, BitMask, extract_levels

__author__ = "Filip Koprivec"


def maxCycleTreeIndependentSet(T: List[List[int]], w: List[List[int]]) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Najtežja neodvisna množica
    v kartezičnem produktu cikla C_k in drevesa T z n vozlišči,
    kjer ima tabela tež w dimenzije k×n (k >= 2).

    Vrne par (c, s), kjer je c teža najdene neodvisne množice,
    s pa je seznam vozlišč v neodvisni množici,
    torej seznam parov oblike (i, u) (0 <= i <= k-1, 0 <= u <= n-1).
    """
    n = len(T)
    assert all(len(r) == n for r in w), "Dimenzije tabele tež ne ustrezajo številu vozlišč v drevesu!"
    assert all(all(u in T[v] for v in a) for u, a in enumerate(T)), "Podani graf ni neusmerjen!"

    k = len(w)
    assert k >= 2, "k mora biti vsaj 2!"

    if n == 0:
        return 0, []

    def calculate_weight(bitmask: BitMask, j: int) -> int:
        su = 0
        for i in range(n):
            if 1 << i & bitmask:
                su += w[i][j]
        return su

    # Calculate levels

    levels, levels_of, parents, children = extract_levels(T)

    # for j in range(len(levels_of)):
    #    assert j in levels[levels_of[j]]

    bitmasks = generate_bitmasks(k)
    transitions = make_transitions(bitmasks)

    # DP[i,b]
    DP = {}  # type: Dict[Tuple[int, BitMask], int]

    MIN_INF = float("-inf")

    # level_i = len(levels) - 1
    for vertex in levels[-1]:
        for mask in bitmasks:
            DP[(vertex, mask)] = calculate_weight(mask, vertex)

    for level_i in range(len(levels) - 2, -1, -1):
        vertexes = levels[level_i]
        for vertex in vertexes:
            for my_mask in bitmasks:  # bitmask on me
                my_cost = calculate_weight(my_mask, vertex)
                DP[(vertex, my_mask)] = my_cost  # My cost
                if not children[vertex]:
                    # We could set ma = 0, but no restraint is given on weights
                    continue

                cur = 0
                for child in children[vertex]:
                    ma = MIN_INF
                    for compatible_mask in transitions[my_mask]:
                        ma = max(DP[(child, compatible_mask)], ma)
                    cur += ma  # type: ignore
                DP[(vertex, my_mask)] += cur

    ma = max(DP[(0, mask)] for mask in bitmasks)

    return ma, []
