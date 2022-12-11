PRIORITY: dict[str, int] = {}

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

for i, letter in enumerate(letters, start=1):
    PRIORITY[letter] = i


def split_in_half(items: list[str]) -> list[tuple[str, str]]:
    list_of_half: list[tuple[str, str]] = []
    for item in items:
        list_of_half.append((item[: len(item) // 2], item[len(item) // 2 :]))
    return list_of_half


def search_in_both(grouped_items: tuple[str, str]) -> str:
    first, second = grouped_items
    intersect = set(first).intersection(set(second))
    return str(intersect.pop())


def search_common_items(items: list[str]) -> str:
    intersection = set(items[0]).intersection(set(items[1])).intersection(set(items[2]))
    return str(intersection.pop())


def parse_tuples(items: list[tuple[str, str]]) -> list[str]:
    return [search_in_both(item) for item in items]


def priority_points(intersections: list[str], priority_dict: dict[str, int]) -> int:
    points = 0
    for item in intersections:
        points += priority_dict[item]
    return points


def parse(raw: str) -> list[str]:
    return raw.strip().split("\n")


def main() -> None:
    with open("day03/data03.txt", "r", encoding="utf-8") as f:
        raw = f.read()
    data = parse(raw)
    # part A
    halfs = split_in_half(data)
    intersections = parse_tuples(halfs)
    total_points = priority_points(intersections, PRIORITY)
    print(total_points)

    # part B
    part_b_intersections: list[str] = []
    j: int = 0
    while j < len(data):
        group = data[i : i + 3]
        part_b_intersections.append(search_common_items(group))
        j += 3
    part_b_points = priority_points(part_b_intersections, PRIORITY)
    print(part_b_points)


if __name__ == "__main__":
    main()
