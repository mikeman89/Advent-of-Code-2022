"""day 04 from advent of code"""


def parse_raw(raw: str) -> list[tuple[set[int], set[int]]]:
    """parse the raw data from the puzzle"""
    data = raw.split("\n")
    ranges: list[tuple[str, str]] = []
    for line in data:
        line_a, line_b = line.strip().split(",")
        ranges.append((line_a, line_b))
    final_list: list[tuple[set[int], set[int]]] = []
    for item in ranges:
        i, j = item
        # first part of jobs
        i_a, i_b = i.split("-")
        set_a: set[int] = set(range(int(i_a), int(i_b) + 1))
        j_a, j_b = j.split("-")
        set_b: set[int] = set(range(int(j_a), int(j_b) + 1))
        final_list.append((set_a, set_b))
    return final_list


def check_for_subset(jobs: tuple[set[int], set[int]]) -> bool:
    """checks if the sets are subsets"""
    set_1, set_2 = jobs
    if set_1.issubset(set_2) or set_2.issubset(set_1):
        return True
    return False


def check_for_overlap(jobs: tuple[set[int], set[int]]) -> bool:
    """checks if the sets are overlapped at all"""
    set_1, set_2 = jobs
    if bool(set_1 & set_2):
        return True
    return False


def main() -> None:
    """main function for the script/file"""
    with open("day04/day04.txt", "r", encoding="UTF-8") as file:
        raw_data = file.read()
    data = parse_raw(raw_data)
    overlaps: int = 0
    for job in data:
        if check_for_overlap(job):
            overlaps += 1
    print(overlaps)


if __name__ == "__main__":
    main()
