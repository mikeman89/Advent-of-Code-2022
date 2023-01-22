from dataclasses import dataclass
from itertools import cycle

XY = tuple[int, int]


@dataclass
class Rock:
    """Treat me as immutable"""

    bottom_left: XY
    offsets: list[XY]

    def points(self) -> set[XY]:
        bx, by = self.bottom_left
        return {(bx + x, by + y) for x, y in self.offsets}

    def move(self, dx: int, dy: int) -> "Rock":
        bx, by = self.bottom_left
        return Rock((bx + dx, by + dy), self.offsets)


OFFSETS = {
    # positive x is right positive y is up
    "-": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "+": [(1, 2), (0, 1), (1, 1), (2, 1), (1, 0)],
    "L": [(2, 2), (2, 1), (2, 0), (0, 0), (1, 0)],
    "I": [(0, 3), (0, 2), (0, 1), (0, 0)],
    "b": [(0, 1), (1, 1), (0, 0), (1, 0)],
}

# 1234567#
# wall at (0, h) for all h
# wall at (8, h) for all h
# piece starts at (3, h) for whatever h


def run(pattern: str, num_steps: int) -> int:
    """return the height of the tallest rock adfter num_steps"""
    occupied: set[XY] = set()
    gasses = cycle(pattern)
    num_rocks = 0

    for rock_type in cycle(OFFSETS):
        if num_rocks >= num_steps:
            return max(y for x, y in occupied)
        else:
            num_rocks += 1
        floor = max(y for x, y in occupied) if occupied else 0
        bottom_left = (3, floor + 4)
        rock = Rock(bottom_left, OFFSETS[rock_type])

        while True:
            # blow with gas
            gas = next(gasses)
            if gas == "<":
                dx, dy = -1, 0
            elif gas == ">":
                dx, dy = 1, 0
            else:
                raise ValueError(f"bad gas: {gas}")
            moved_rock = rock.move(dx, dy)
            points = moved_rock.points()
            if (
                any(x <= 0 for x, y in points)
                or any(x >= 8 for x, y in points)
                or (points & occupied)
            ):
                # hit another rock or wall
                pass
            else:
                rock = moved_rock
            # try to fall
            moved_rock = rock.move(0, -1)
            points = moved_rock.points()
            if any(y <= 0 for x, y in points) or (points & occupied):
                # add all points to the occupied set
                occupied = occupied | rock.points()
                break  # out of while loop
            else:
                rock = moved_rock
    return max(y for x, y in occupied)


def main():
    with open("day17/day17.txt", "r", encoding="UTF-8") as data:
        gasses = data.read()

    max_height: int = run(gasses, 2022)
    print(max_height)


if __name__ == "__main__":
    main()
