from dataclasses import dataclass


@dataclass
class Elf:
    food: list[int]

    def cals(self) -> int:
        return sum(self.food)


def parse(raw: str) -> list[Elf]:
    return [
        Elf([int(x) for x in line.split('\n')])
        for line in raw.split('\n\n')
    ]


def max_cals(elves: list[Elf]) -> int:
    return max([elf.cals() for elf in elves])


def sorted_cals(elves: list[Elf]) -> list[int]:
    return sorted([elf.cals() for elf in elves], reverse=True)


def top_3(calories: list[int]) -> int:
    return sum(calories[:3])


def main() -> None:
    with open("data01.txt", "r") as f:
        RAW = f.read()
    elves = parse(RAW)
    # for the elf with the most calories
    max_calories = max_cals(elves)
    print(max_calories)

    # for the top 3 elves with the most calories
    sorted_calories = sorted_cals(elves)
    top_3_cals = top_3(sorted_calories)
    print(top_3_cals)


if __name__ == "__main__":
    main()
