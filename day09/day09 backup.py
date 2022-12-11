from dataclasses import dataclass, field


def parse(raw: str) -> list[tuple[str, int]]:
    movement: list[tuple[str, int]] = []
    for line in raw.split("\n"):
        direction, distance = line.split()[0], line.split()[1]
        movement.append((direction, int(distance)))

    return movement


@dataclass
class Knot:
    x: int = 0
    y: int = 0
    history: list[tuple[int, int]] = field(default_factory=lambda: [(0, 0)])

    def add_to_history(self) -> None:
        self.history.append((self.x, self.y))

    def count_locations(self) -> int:
        return len(set(self.history))

    def move_head(self, direction: str) -> None:
        if direction == "R":
            self.x += 1
        if direction == "U":
            self.y += 1
        if direction == "L":
            self.x -= 1
        if direction == "D":
            self.y -= 1


def move_tail(head: Knot, tail: Knot) -> Knot:
    if (
        (head.x - tail.x == 2)
        and (head.y - tail.y == 1)
        or (head.x - tail.x == 1)
        and (head.y - tail.y == 2)
    ):
        tail.y += 1
        tail.x += 1
    elif (
        (head.x - tail.x == -2)
        and (head.y - tail.y == 1)
        or (head.x - tail.x == -1)
        and (head.y - tail.y == 2)
    ):
        tail.y += 1
        tail.x -= 1
    elif (
        (head.x - tail.x == -2)
        and (head.y - tail.y == -1)
        or (head.x - tail.x == -1)
        and (head.y - tail.y == -2)
    ):
        tail.y -= 1
        tail.x -= 1
    elif (
        (head.x - tail.x == 2)
        and (head.y - tail.y == -1)
        or (head.x - tail.x == 1)
        and (head.y - tail.y == -2)
    ):
        tail.y -= 1
        tail.x += 1
    elif head.x - tail.x == 2:
        tail.x += 1
    elif head.x - tail.x == -2:
        tail.x -= 1
    elif head.y - tail.y == 2:
        tail.y += 1
    elif head.y - tail.y == -2:
        tail.y -= 1
    else:
        pass
    return tail


def main() -> None:
    with open("day09/day09.txt", "r", encoding="UTF-8") as file_data:
        raw = file_data.read()
    head = Knot()
    tail1 = Knot()
    tail2 = Knot()
    tail3 = Knot()
    tail4 = Knot()
    tail5 = Knot()
    tail6 = Knot()
    tail7 = Knot()
    tail8 = Knot()
    tail9 = Knot()
    moves = parse(raw)
    for direction, distance in moves:
        for _ in range(distance):
            head.move_head(direction)
            move_tail(head, tail1)
            move_tail(tail1, tail2)
            move_tail(tail2, tail3)
            move_tail(tail3, tail4)
            move_tail(tail4, tail5)
            move_tail(tail5, tail6)
            move_tail(tail6, tail7)
            move_tail(tail7, tail8)
            move_tail(tail8, tail9)
            tail9.add_to_history()

    print(tail9.count_locations())


if __name__ == "__main__":
    main()
