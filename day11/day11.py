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
            if worry % self.test == 0:
                yield (self.iftrue, worry)
            else:
                yield (self.iffalse, worry)


def parse(raw: str, worry_divisor: int) -> list[Monkey]:
    return [Monkey(monkey_do, worry_divisor) for monkey_do in raw.split("\n\n")]


def play_a_round(monkeys: list[Monkey]) -> list[Monkey]:
    for monkey in monkeys:
        for catcher, worry in monkey.play():
            monkeys[catcher].items.append(worry)
    return monkeys


def main() -> None:
    pass


if __name__ == "__main__":
    main()
