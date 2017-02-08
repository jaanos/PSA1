# -*- coding: utf-8 -*-

from collections import deque

from typing import Dict
from typing import Tuple, List
from .helpers import generate_bitmasks, make_transitions, BitMask, extract_levels, generate_product_with_bitmask

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
        for i in range(k):
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
    # max wight where i is parent and is assigned bitmask b
    # Also saves which bitmask is assigned to specific child
    DP = {}  # type: Dict[Tuple[int, BitMask], Tuple[int, List[BitMask]]]

    MIN_INF = float("-inf")

    # level_i = len(levels) - 1
    for vertex in levels[-1]:
        for mask in bitmasks:
            #                                                    # no mask down from me
            temp = []  # type: List[BitMask]
            DP[(vertex, mask)] = calculate_weight(mask, vertex), temp

    for level_i in range(len(levels) - 2, -1, -1):
        vertexes = levels[level_i]
        for vertex in vertexes:
            for my_mask in bitmasks:  # bitmask on me
                my_cost = calculate_weight(my_mask, vertex)
                if not children[vertex]:
                    DP[(vertex, my_mask)] = my_cost, []
                    continue

                submasks = []  # type: List[BitMask]
                cur = 0
                for child in children[vertex]:
                    ma = MIN_INF
                    cur_mask = None
                    for compatible_mask in transitions[my_mask]:
                        dp, _ = DP[(child, compatible_mask)]
                        if dp > ma:
                            ma = dp
                            cur_mask = compatible_mask
                    cur += int(ma)
                    assert cur_mask is not None
                    submasks.append(cur_mask)

                DP[(vertex, my_mask)] = my_cost + cur, submasks

    m, obj = calculate_graph(DP, children, bitmasks)

    su = 0
    for i, j in obj:
        su += w[i][j]
    assert su == m

    return m, obj

    # return int(ma), []


def calculate_graph(DP: Dict[Tuple[int, BitMask], Tuple[int, List[BitMask]]], children: List[List[int]],
                    bitmasks: List[BitMask]) -> Tuple[int, List[Tuple[int, int]]]:
    def get_best_on_index(ind: int) -> Tuple[int, BitMask]:
        ma = float("-inf")
        best_mask = None
        for mask in bitmasks:
            val, children = DP[(ind, mask)]
            if val > ma:
                ma = DP[(0, mask)][0]
                best_mask = mask

        assert best_mask is not None

        return int(ma), best_mask

    calculated_zero_max, best_starting_mask = get_best_on_index(0)

    rtr = []  # type: List[Tuple[int, int]]

    queue = deque([(0, best_starting_mask)])

    while queue:
        ind, best_mask = queue.popleft()
        rtr.extend(generate_product_with_bitmask(best_mask, ind))

        _, children_masks = DP[(ind, best_mask)]

        for j in range(len(children[ind])):
            queue.append((children[ind][j], children_masks[j]))

    return int(calculated_zero_max), rtr
