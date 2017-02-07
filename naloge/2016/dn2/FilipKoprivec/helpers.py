# -*- coding: utf-8 -*-

"""Helper functions"""

from typing import List, Dict, NewType, Tuple, Optional

__author__ = "Filip Koprivec"

BitMask = NewType("BitMask", int)


def generate_bitmasks_with_exp(n: int) -> List[BitMask]:
    waiting = [BitMask(1)]
    valid = [BitMask(0)]
    for j in range(1, n):
        temp = []
        for k in valid:
            temp.append(BitMask(k | 2 ** j))
        valid.extend(waiting)
        waiting = temp
    return valid + waiting


def are_compatible(x: BitMask, y: BitMask) -> bool:
    return x & y == 0


def make_transitions(bitmasks: List[BitMask]) -> Dict[BitMask, List[BitMask]]:
    return {j: [i for i in bitmasks if are_compatible(j, i)] for j in bitmasks}


def generate_bitmasks_with_shift(n: int) -> List[BitMask]:
    waiting = [BitMask(1)]
    valid = [BitMask(0)]
    for j in range(1, n - 1):
        val = 1 << j
        temp = []
        for k in valid:
            temp.append(BitMask(k | val))
        valid.extend(waiting)
        waiting = temp
    # Last one
    val = 1 << n - 1
    temp = []
    for k in valid:
        if not k & 1:  # Don't include last one
            temp.append(BitMask(k | val))
    valid.extend(waiting)

    return valid + temp


def generate_bitmasks_with_multiplication(n: int) -> List[BitMask]:
    waiting = [BitMask(1)]
    valid = [BitMask(0)]
    val = 1
    for j in range(1, n - 1):
        val *= 2  # not mush faster than val = 1 << j
        temp = []
        for k in valid:
            temp.append(BitMask(k | val))
        valid.extend(waiting)
        waiting = temp

    # Last one
    val *= 2
    temp = []
    for k in valid:
        if not k & 1:  # Don't include last one
            temp.append(BitMask(k | val))
    valid.extend(waiting)

    return valid + temp


def test_bitmask(bitmask: int, l: int) -> bool:
    s_mask = (bin(bitmask)[2:]).zfill(l)
    if len(s_mask) == 1:
        return True
    for j in range(len(s_mask) - 1):
        if s_mask[j] == "1" and s_mask[j + 1] == "1":
            return False
    return s_mask[0] != "1" or s_mask[-1] != "1"


def slow_version(n: int) -> List[int]:
    return [k for k in range(2 ** n) if test_bitmask(k, n)]


def test_generate_bitmasks(N: int = 10) -> bool:
    for j in range(2, N):
        correct = slow_version(j)
        shift = generate_bitmasks_with_shift(j)
        multi = generate_bitmasks_with_multiplication(j)
        assert list(sorted(correct)) == list(sorted(shift)) == list(sorted(multi))
    return True


def time_generation(N: int = 30) -> None:
    from time import time
    for j in range(2, N):
        t = time()
        l1 = len(generate_bitmasks(j))
        normal = time() - t
        t = time()
        l2 = len(generate_bitmasks_with_shift(j))
        shift = time() - t
        assert l1 == l2
        t = time()
        l3 = len(generate_bitmasks_with_multiplication(j))
        multi = time() - t
        print(j, l1, normal, shift, multi, normal - shift, shift / (normal or 1))


# Save the best
generate_bitmasks = generate_bitmasks_with_multiplication


def extract_levels(graph: List[List[int]]) -> Tuple[List[List[int]], List[int], List[int], List[List[int]]]:
    # Not asymptotically optimal, but in amortized case fast enough
    stack = []
    levels = []  # type: List[List[int]]
    level_of = [0 for _ in range(len(graph))]
    visited = [False for _ in range(len(graph))]

    # modified graph, tuple of (Parent, [Children]) for each vertex
    children = [[] for j in range(len(graph))]  # type: List[List[int]]
    parents = [0 for j in range(len(graph))]

    it = iter([0])
    v = None
    u = None

    cur_level = -1

    def previsit(u: int, v: Optional[int]) -> None:
        nonlocal cur_level
        cur_level += 1
        if len(levels) <= cur_level:
            levels.append([u])
        else:
            levels[cur_level].append(u)
        parents[u] = v  # type: ignore
        if v is not None:
            children[v].append(u)
        level_of[u] = cur_level

    def postvisit() -> None:
        nonlocal cur_level
        cur_level -= 1

    while 1:
        try:
            u = next(it)
        except StopIteration:
            if v is None:
                break
            u = v
            v, it = stack.pop()
            postvisit()
            continue
        if visited[u]:
            continue
        visited[u] = True
        previsit(u, v)
        stack.append((v, it))
        v, it = u, iter(graph[u])

    return levels, level_of, parents, children


def main(n: int = 4, N: int = 20) -> None:
    print(list(sorted(slow_version(n))))
    print(list(sorted(generate_bitmasks(n))))
    print(list(sorted(generate_bitmasks_with_shift(n))))
    for j in slow_version(n):
        print((bin(j)[2:]).zfill(n))

    test_generate_bitmasks(N)


if __name__ == '__main__':
    main()
    time_generation()
