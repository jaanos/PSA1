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

    # We are operating on a tree -> n = V = E + 1 => O(V) = (E) = O(E+V)

    # For analysis, assume: len(bitmask) as "usable" length of bitmask (maximum over all most significant bits set)
    # We can easily see, that it will be bounded by k and so int(bitmask) <= 2**k

    def calculate_weight(bitmask: BitMask, j: int) -> int:  # Cost: O(len(bitmask)) = O(k), memory: O(1)
        su = 0
        for i in range(k):
            if 1 << i & bitmask:
                su += w[i][j]
        return su

    # Calculate levels

    # Cost: time, memory O(n)
    levels, levels_of, parents, children = extract_levels(T)

    # Generate possible transitions, let B be the number of bitmasks, rough estimate is that B = O(2**k)
    # But for better estimates let B be the number of bitmasks
    bitmasks = generate_bitmasks(k)  # Cost: O(B), memory: O(B) for saving all bitmasks
    # Let T be the number of all transitions, we know T = O(B^2), but can be a bit smaller,
    # but not much, as at least half valid states are compatible from every state
    transitions = make_transitions(bitmasks)  # Cost: O(B^2), memory: O(T)

    # DP[i,b]
    # max weight of subtree with parent i that is assigned bitmask b
    # Also saves which bitmask is assigned to specific child
    DP = {}  # type: Dict[Tuple[int, BitMask], Tuple[int, List[BitMask]]]  # Cost: O(1),
    # memory: assuming good behaved dictionary, will store up to n*B, entries, where each entry will consist of
    # int(max value) and bitmask used for obtaining this value for each child of i

    # for each bitmask, we wil store n elements (as keys) and also additional n pointers to children
    # So total memory cost of dict: O(B*(n+n)) = O(B*n)

    # Preparations cost:
    # Time: O(n) + O(B) + O(B^2) = O(n + B^2)
    # Memory: O(n) + O(B) + O(T) = O(B^2)
    # But not so much memory, as BitMasks are ints

    MIN_INF = float("-inf")

    # level_i = len(levels) - 1
    # Check lowest level, in time analysis, just merge it with next loop
    for vertex in levels[-1]:
        for mask in bitmasks:
            #                                                    # no mask down from me
            temp = []  # type: List[BitMask]
            DP[(vertex, mask)] = calculate_weight(mask, vertex), temp

    for level_i in range(len(levels) - 2, -1, -1):  # Go by depth in tree
        vertexes = levels[level_i]
        for vertex in vertexes:  # Check each vertex  # So together we have n operations here

            # After loop reforming -> O(n (children) * B (my_mask) * B (compatible_mask[my_mask]))
            # small_dp_cost = n*B^2 operations

            # list submasks holds at most n children at any time: memory O(n)

            # Check all bitmasks
            # We need to check B things
            for my_mask in bitmasks:  # bitmask on me
                my_cost = calculate_weight(my_mask, vertex)
                if not children[vertex]:  # Leaf of tree, all costs constant
                    DP[(vertex, my_mask)] = my_cost, []
                    continue

                submasks = []  # type: List[BitMask]
                cur = 0
                # Dynamic programming
                # For each children
                for child in children[vertex]:
                    # At most n vertices will be checked at all (looking from for vertex in vertices)
                    ma = MIN_INF
                    cur_mask = None
                    # Get max by compatible mask
                    for compatible_mask in transitions[my_mask]:  # At most O(B), if my_mask = 0, we need to check all
                        dp, _ = DP[(child, compatible_mask)]
                        if dp > ma:
                            ma = dp
                            cur_mask = compatible_mask
                    # And sum all children
                    cur += int(ma)
                    assert cur_mask is not None
                    submasks.append(cur_mask)

                DP[(vertex, my_mask)] = my_cost + cur, submasks

    # full cost of loops: Outer loop : n * small_dp_cost = n^2*B^2 => O(n^2 * B^2)

    # Computation cost:
    # Preparations cost + Outer loop
    # Time: O(n + B^2) + O(n^2 + B^2) = O(n^2 * B^2) = approx = O(n^2 * 2^(2k)) = O(n^2 * 4^k)
    # Space: O(B^2) + O(B*n)

    # Backtrack path
    # Cost: O(n*k), space: O(n*k)
    m, obj = calculate_graph(DP, children, bitmasks)

    # Total cost:
    # Time: O(n^2 * B^2) = approx = O(n^2 * 2^(2k)) = O(n^2 * 4^k)
    # Space: O(B^2) + O(B*n) = approx = O(4^k) + O(2^k*n)
    return m, obj


# Cost: time: O(n*k), space: O(n*k)
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

    # Get best mask on level 0
    # Cost: O(B)
    calculated_zero_max, best_starting_mask = get_best_on_index(0)

    # Return all vertices in best graph
    # max size: O(k*n), take half in each level -> k*n/2
    rtr = []  # type: List[Tuple[int, int]]

    # Guaranteed O(1) pop and insertion on both endpoints (by the documentation and design of the queue)
    # memory: O(n)
    queue = deque([(0, best_starting_mask)])

    # Do a BFS, cost: O(n), space: O(n*k) for size of rtr

    while queue:
        ind, best_mask = queue.popleft()
        # Cost: time, memory: O(k)
        rtr.extend(generate_product_with_bitmask(best_mask, ind))

        _, children_masks = DP[(ind, best_mask)]

        # For each children, across whole while loop at most n (the runtime of while loop)
        for j in range(len(children[ind])):
            queue.append((children[ind][j], children_masks[j]))

    return int(calculated_zero_max), rtr
