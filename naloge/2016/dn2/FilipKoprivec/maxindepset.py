# -*- coding: utf-8 -*-

from collections import deque

from typing import Tuple, List
from .helpers import generate_bitmasks, make_transitions, BitMask, extract_levels, generate_product_with_bitmask

__author__ = "Filip Koprivec"


def maxCycleTreeIndependentSet(T: List[List[int]], w: List[List[int]], assert_sum: bool = False) -> Tuple[int, List[Tuple[int, int]]]:
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

    # let sq2 denote square root of 2 (sq2 = 2**0.5 = approx = 1.414)
    # let sq21 denote sq2 + 1 (2**0.5 + 1 = approx = 2.414)
    # let phi denote golden ratio ( (1 + 5**0.5)/2 = approx = 1.618)

    # Calculate levels

    # Cost: time, memory O(n)
    levels, parents, children = extract_levels(T)

    # Generate possible transitions, let B be the number of bitmasks, rough estimate is that B = O(2**k)
    # But for better estimates let B be the number of bitmasks

    # More thorough analysis of B:
    # Consider all sequences ob bits ({0,1}) with length k, so that no two adjacent bits are set, call them BB
    # and let A(n) be number of such bits
    # Also consider subformula for it, A(n,0) and A(n,1) are number of sequences of length n, ending with 0 or 1,
    # clearly A(n) = A(n, 0) + A(n, 1)
    # We can se that A(n+1, 0) = A(n, 0) + A(n, 1) = A(n), (by setting last bit to 0), also
    # A(n+1, 1) = A(n, 0) = A(n-1, 0) + A(n-1, 1) = A(n-1)
    # From here we have recurrence A(n+2) = A(n+1) + A(n) with A(1) = 2 and A(2) = 3
    # We have A, as shifted fibonacci numbers A(n) = F(n+2) // if we use F(1) = F(2) = 1
    # So we have asymptotically A = O(phi^n)
    # We therefore have: len(BB(n)) = O(phi^n)
    # As the set of bitmasks is under BB (BB alows that first and last bit are both set, while bitmasks do not).
    # We also have B = O(phi^k) = approx = O(1.618^k)

    # If we limit the len of bitmasks even more, we find out, that B(i) = F(i+2) - F(i-2) // Assuming F(0) = 0, F(1) = 1
    # We don't want sequences that start with 1 and end with one, by simply writing the recurrence with 3 indexes
    # (instead of 2), we can se, that F(i-4) sequences are "undesirable", to get B(i) = F(i+2) - F(i-2) we simply shift
    # starting point as before
    # We can rearrange this to get B(i) = B(i-1) + B(i-2) and we get fibonacci sequence, but with a different starting
    # point, so we are still in the same complexity class.

    bitmasks = generate_bitmasks(k)  # Cost: O(B), memory: O(B) for saving all bitmasks
    # Let T be the number of all transitions, we know O(T) = O(B^2), but more precise analysis of make_translations
    # establishes, that O(T) = O(sq21^k) = approx = O(2.4142^k)
    transitions = make_transitions(bitmasks)  # Cost: O(B^2), memory: O(T)

    # DP[i][b]
    # max weight of subtree with parent i that is assigned bitmask b
    # Also saves which bitmask is assigned to specific child
    # Cost: O(n)
    B = len(bitmasks)
    # Cache range(B
    range_b = range(B)
    DP = [[(0, []) for _ in range_b] for _ in range(n)]  # type: List[List[Tuple[int, List[int]]]]
    # memory: assuming good behaved dictionary, will store up to n*B, entries, where each entry will consist of
    # int(max value) and bitmask used for obtaining this value for each child of i

    # for each bitmask, we wil store n elements (as keys) and also additional n pointers to children
    # So total memory cost of dict: O(B*(n+n)) = O(B*n)

    # Preparations cost:
    # Time: O(n) + O(B) + O(B^2) = O(n + B^2)
    # Memory: O(n) + O(B) + O(T) = O(T)
    # But not so much memory, as BitMasks are ints

    MIN_INF = float("-inf")

    # Cache range(k)
    range_k = range(k)

    def calculate_weight(bitmask: BitMask, j: int) -> int:  # Cost: O(len(bitmask)) = O(k), memory: O(1)
        # return sum(w[i][j] for i in range(k) if 1 << i & bitmask)
        su = 0
        for i in range_k:
            if 1 << i & bitmask:
                su += w[i][j]
        return su

    # level_i = len(levels) - 1
    # Check lowest level, in time analysis, just merge it with next loop
    for vertex in levels[-1]:
        for mask_i, mask in enumerate(bitmasks):
            #                                                    # no mask down from me
            temp = []  # type: List[int]
            DP[vertex][mask_i] = calculate_weight(mask, vertex), temp

    for level_i in range(len(levels) - 2, -1, -1):  # Go by depth in tree
        vertexes = levels[level_i]
        for vertex in vertexes:  # Check each vertex  # So together we have n operations here

            # Pre indexing takes O(1) time (list indexing is constant) and O(1) space (one more reference)
            # Pre index to speed up inner loops
            DP_vertex = DP[vertex]

            # And with subloop children checking, we will count each vertex twice, first as parent, and then as child
            # of his parent, so running time is linear in n

            # After loop reforming -> O(T) + cost of children

            # list submasks holds at most n children at any time: memory O(n)

            # Check all bitmasks
            # We only check all bitmasks in transitions.values(), not all possible pairwise combinations ob bitmasks
            # This is certain lower than O(B^2), but is more precisely O(T)
            for my_mask_i, my_mask in enumerate(bitmasks):  # bitmask on me
                my_cost = calculate_weight(my_mask, vertex)
                if not children[vertex]:  # Leaf of tree, all costs constant
                    DP_vertex[my_mask_i] = my_cost, []
                    continue

                # Save optimal submasks for children
                optimal_submasks = []  # type: List[int]
                cur = 0
                # Dynamic programming
                # For each children
                for child in children[vertex]:
                    # Check all my children
                    ma = MIN_INF
                    cur_mask_i = None

                    # Pre index to speed up inner loop
                    DP_child = DP[child]

                    # Get max by compatible mask
                    for compatible_mask_i in transitions[my_mask_i]:  # At most O(B), if my_mask = 0, we need to check all
                        dp, _ = DP_child[compatible_mask_i]
                        if dp > ma:
                            ma = dp
                            cur_mask_i = compatible_mask_i
                    # And sum all children
                    cur += int(ma)
                    assert cur_mask_i is not None
                    optimal_submasks.append(cur_mask_i)

                DP_vertex[my_mask_i] = my_cost + cur, optimal_submasks

    # full cost of loops: n*T => O(n * T)

    # Computation cost:
    # Preparations cost +  Outer loop
    # Time: O(n + B^2)  +  O(n * T) = O(n + B^2) + O(n * T) = approx = O(n * 2.414^k) + O(1.618^(2k))
    # Space: O(T)       +  O(B*n) = approx = O(2.414^k) + O(phi^k*n)

    # Backtrack path
    # Cost: O(n*k + B), space: O(n*k)
    m, obj = calculate_graph(DP, children, bitmasks)

    # Total cost:
    # Time: O(n * T + B^2) = O(n * sq21^k + phi^(2*k)) = approx = O(2.826^k + n * 2.414^k)
    # Space: O(T) + O(B*n) = O(sq21^k) + O(phi^k*n) = O(sq21^k + phi^k*n) = approx = O(2.414^k + 1.618^k*n)

    # Ignore this in analysis
    if assert_sum:
        su = sum(w[i][j] for i, j in obj)
        assert su == m
        print("Assert OK")

    return m, obj


# Cost: time: O(n*k + B), space: O(n*k)
def calculate_graph(DP: List[List[Tuple[int, List[int]]]], children: List[List[int]],
                    bitmasks: List[BitMask]) -> Tuple[int, List[Tuple[int, int]]]:

    def get_best_on_index(ind: int) -> Tuple[int, int]:
        ma = float("-inf")
        best_mask_i = None
        for mask_i, mask in enumerate(bitmasks):
            val, children = DP[ind][mask_i]
            if val > ma:
                ma = DP[0][mask_i][0]
                best_mask_i = mask_i

        assert best_mask_i is not None

        return int(ma), best_mask_i

    # Get best mask on level 0
    # Cost: O(B)
    # We pay this cost, because we have to check for the best bitmask we want to use on root
    # We could go around (but still pay for it), by adding another root and setting its bitmask on zero, so that
    # DP will do this work
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
        rtr.extend(generate_product_with_bitmask(bitmasks[best_mask], ind))

        _, children_masks = DP[ind][best_mask]

        # For each children, across whole while loop at most n (the runtime of while loop)
        for j in range(len(children[ind])):
            queue.append((children[ind][j], children_masks[j]))

    return int(calculated_zero_max), rtr
