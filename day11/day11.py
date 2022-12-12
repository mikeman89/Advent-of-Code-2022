from functools import reduce
from typing import Callable, Iterator


class Monkey:
    def __init__(self, monkey_do: str, worry_divisor: int) -> None:
        monkey_data = monkey_do.splitlines()
        self.worry_divisor: int = worry_divisor
        self.items: list[int] = eval("[" + monkey_data[1][18:] + "]")
        self.operation: Callable[[int], int] = eval(
            "lambda old: " + monkey_data[2][19:]
        )
        self.test: int = int(monkey_data[3][21:])
        self.iftrue: int = int(monkey_data[4][-1])
        self.iffalse: int = int(monkey_data[5][-1])
        self.inspect_count: int = 0

    def play(self) -> Iterator[tuple[int, int]]:
        while self.items:
            self.inspect_count += 1
            worry = self.operation(self.items.pop(0)) // self.worry_divisor
            if worry % self.test:
                yield self.iffalse, worry % 9_699_690 if self.worry_divisor == 1 else worry
            else:
                yield self.iftrue, worry


def parse(raw: str, worry_divisor: int) -> list[Monkey]:
    return [Monkey(monkey_do, worry_divisor) for monkey_do in raw.split("\n\n")]


def play_a_round(monkeys: list[Monkey]) -> list[Monkey]:
    for monkey in monkeys:
        for catcher, worry in monkey.play():
            monkeys[catcher].items.append(worry)
    return monkeys


def play_a_game(monkeys: list[Monkey], rounds: int) -> int:
    for _ in range(rounds):
        monkeys = play_a_round(monkeys)

    inspect_sorted: list[int] = sorted(
        [monkey.inspect_count for monkey in monkeys], reverse=True
    )

    return inspect_sorted[0] * inspect_sorted[1]


def main() -> None:
    with open("day11/day11.txt", "r", encoding="UTF-8") as file_data:
        raw = file_data.read()
    monkeys = parse(raw, 1)
    game_points = play_a_game(monkeys, 10_000)
    print(game_points)


if __name__ == "__main__":
    main()
