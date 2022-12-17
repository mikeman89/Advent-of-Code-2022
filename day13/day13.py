# pylint: disable=missing-class-docstring,missing-function-docstring,missing-module-docstring

from functools import cmp_to_key
from itertools import zip_longest
from typing import Any

Packet = list[Any]
Pair = tuple[Packet, Packet]


def parse(raw: str) -> list[Pair]:
    pairs = []
    for pair in raw.split("\n\n"):
        p1, p2 = pair.split("\n")
        pairs.append((eval(p1), eval(p2)))
    return pairs


def parse_part_2(raw: str) -> list[Packet]:
    pairs = []
    for pair in raw.split("\n\n"):
        p1, p2 = pair.split("\n")
        pairs.append(eval(p1))
        pairs.append(eval(p2))
    pairs.append([[2]])
    pairs.append([[6]])
    return pairs


def compare(p1: Packet, p2: Packet) -> int:
    """Are the packets in the right order"""
    match (p1, p2):
        case (int(), int()):
            if p1 < p2:
                return 1  # good
            if p1 > p2:
                return -1  # bad

            return 0  # continue checking
        case (list(), int()):
            return compare(p1, [p2])
        case (int(), list()):
            return compare([p1], p2)
        case (list(), list()):
            for a, b in zip_longest(p1, p2):
                if a is None:
                    # a ran out of items first
                    return 1
                if b is None:
                    # b ran out first
                    return -1
                # neither ran out first
                result = compare(a, b)
                if result != 0:
                    return result
            # got to the end and none of these happened
            return 0


def right_order_sum(pairs: list[Pair]) -> int:
    res: int = 0
    for i, (p1, p2) in enumerate(pairs, 1):
        result = compare(p1, p2)
        if result == 1:
            res += i
    return res


def find_2_6(sorted_packet: list[Packet]) -> int:
    res = 1
    for i, packet in enumerate(sorted_packet, 1):
        if packet == [[2]]:
            res *= i
        elif packet == [[6]]:
            res *= i
    return res


def main():
    with open("day13/day13.txt", "r", encoding="UTF-8") as data_file:
        raw = data_file.read()
    pairs = parse(raw)
    print(right_order_sum(pairs))

    packets = parse_part_2(raw)
    sorted_packets = sorted(packets, reverse=True, key=cmp_to_key(compare))
    print(find_2_6(sorted_packets))


if __name__ == "__main__":
    main()
