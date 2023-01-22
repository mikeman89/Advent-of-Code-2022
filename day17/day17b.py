from dataclasses import dataclass
from itertools import cycle
from typing import Iterator

import pandas as pd
import tqdm

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


def run(pattern: str) -> Iterator[dict[str, int | bool | None]]:
    """return the height of the tallest rock adfter num_steps"""
    occupied: set[XY] = set()
    gasses = cycle(pattern)
    num_rocks = 0
    height = 0
    h = 0
    deleted = 0

    for rock_type in cycle(OFFSETS):
        num_rocks += 1
        floor = max(y for _, y in occupied) if occupied else 0
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
                any(x <= 0 for x, _ in points)
                or any(x >= 8 for x, _ in points)
                or (points & occupied)
            ):
                # hit another rock or wall
                pass
            else:
                rock = moved_rock
            # try to fall
            moved_rock = rock.move(0, -1)
            points = moved_rock.points()
            # hit the floor or other rocks
            if any(y <= 0 for _, y in points) or (points & occupied):
                # add all points to the occupied set
                occupied = occupied | rock.points()

                height = max(height, max(y for _, y in occupied))
                # check for a full line
                line: list[int] = []
                for _, y in points:
                    if all((x, y) in occupied for x in range(1, 8)):
                        line.append(y)
                if line:
                    h = max(line)
                    # reset to 0
                    occupied = {(x, y - h) for x, y in occupied if y > h}
                    deleted += h
                    height -= h

                yield {
                    "height": height + deleted,
                    "time": num_rocks,
                    "line_completed": bool(line),
                    "delta": h if line else None,
                }

                break  # out of while loop
            else:
                rock = moved_rock


# with open("day17/test_day17.txt", "r", encoding="UTF-8") as data:
#     gasses = data.read()

gasses = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

it = run(gasses)

df = pd.DataFrame([next(it) for _ in tqdm.trange(10_000)])
