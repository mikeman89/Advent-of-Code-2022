# pylint: disable=missing-class-docstring,missing-function-docstring,missing-module-docstring
from typing import Generator

Sensor = tuple[int, int]
Beacon = tuple[int, int]
SensorBeacon = tuple[Sensor, Beacon]
# World = dict[tuple[int, int], str]
MOVES: dict[str, tuple[int, int]] = {
    "NE": (1, 1),
    "SE": (1, -1),
    # "E": (1, 0),
    "SW": (-1, -1),
    # "S": (0, -1),
    # "W": (-1, 0),
    "NW": (-1, 1),
    # "N": (0, 1),
}


def parse(lines: list[str]) -> list[SensorBeacon]:
    sensor_beacon: list[SensorBeacon] = []
    for line in lines:
        line_info = line.split(" ")
        x1 = int(line_info[2].split("=")[1].split(",")[0])
        y1 = int(line_info[3].split("=")[1].split(":")[0])
        x2 = int(line_info[8].split("=")[1].split(",")[0])
        y2 = int(line_info[9].split("=")[1])
        sensor: Sensor = (x1, y1)
        beacon: Beacon = (x2, y2)
        sensor_beacon.append((sensor, beacon))
    return sensor_beacon


def manhatton_distance(sensor_beacon: SensorBeacon) -> int:
    (x1, y1), (x2, y2) = sensor_beacon
    return abs(x1 - x2) + abs(y1 - y2)


def get_min_max_x(sensor_beacons: list[SensorBeacon]) -> tuple[int, int, int]:
    min_x = 100000
    max_x = -100000
    max_delta = 0
    for sensor, beacon in sensor_beacons:
        dist = manhatton_distance((sensor, beacon))
        min_x = min(sensor[0], beacon[0], min_x)
        max_x = max(sensor[0], beacon[0], min_x)
        max_delta = max(max_delta, dist)
    return (min_x, max_x, max_delta)


def no_beacon_in_row(
    row: int, min_x: int, max_x: int, max_delta: int, sensor_beacons: list[SensorBeacon]
) -> int:
    total = 0
    sensors = [sensor for sensor, _ in sensor_beacons]
    beacons = [beacon for _, beacon in sensor_beacons]
    for x in range(min_x - max_delta, max_x + max_delta + 1):

        for sensor, beacon in sensor_beacons:
            p_dist = manhatton_distance(((x, row), sensor))
            if p_dist <= manhatton_distance((sensor, beacon)):
                if (x, row) in sensors or (x, row) in beacons:
                    continue
                total += 1
                break
    return total


# def make_world(sensor_beacons: list[SensorBeacon]) -> World:
#     world: World = {}
#     for sensor_beacon in sensor_beacons:
#         man_dist = manhatton_distance(sensor_beacon)
#         (x1, y1), (x2, y2) = sensor_beacon
#         world[(x1, y1)] = "S"
#         world[(x2, y2)] = "B"
#         for y in range(y1 - man_dist, y1 + man_dist + 1):
#             for x in range(x1 - man_dist, x1 + man_dist + 1):
#                 if (
#                     manhatton_distance(((x1, y1), (x, y))) <= man_dist
#                     and world.get((x, y)) is None
#                 ):
#                     world[(x, y)] = "#"
#     return world


# def show_world(world: World) -> None:
#     min_x = min(x for x, y in world)
#     min_y = min(y for x, y in world)
#     max_x = max(x for x, y in world)
#     max_y = max(y for x, y in world)

#     for y in range(min_y, max_y + 1):
#         for x in range(min_x, max_x + 1):
#             print(world.get((x, y), "."), end="")
#         print()


# def count_no_beacons(row: int, world: World) -> int:
#     count = 0
#     x_min = min(x for x, y in world)
#     x_max = max(x for x, y in world)
#     for x in range(x_min, x_max + 1):
#         if world.get((x, row)) == "#" or world.get((x, row)) == "S":
#             count += 1
#     return count


def generate_points_outside(
    move_list: dict[str, tuple[int, int]],
    sensor_beacons: list[SensorBeacon],
    min_beacon: int,
    max_beacon: int,
) -> Generator[tuple[int, int], None, None]:
    for sensor, beacon in sensor_beacons:
        dist: int = manhatton_distance((sensor, beacon))
        point = (sensor[0] - dist - 1, sensor[1])

        for move in move_list:
            for _ in range(dist):
                point = (
                    point[0] + move_list[move][0],
                    point[1] + move_list[move][1],
                )
                if (
                    min_beacon <= point[0] <= max_beacon
                    and min_beacon <= point[1] <= max_beacon
                ):
                    yield point


def main() -> None:
    with open("day15/day15.txt", "r", encoding="UTF-8") as data_file:
        lines = data_file.readlines()
    sensor_beacons = parse(lines)
    # min_x, max_x, max_delta = get_min_max_x(sensor_beacons)
    # total = no_beacon_in_row(2_000_000, min_x, max_x, max_delta, sensor_beacons)
    # print(total)

    MIN_BEACON = 0
    MAX_BEACON = 4_000_000
    # MAX_BEACON = 20

    for point in generate_points_outside(MOVES, sensor_beacons, MIN_BEACON, MAX_BEACON):
        for sensor, beacon in sensor_beacons:
            pdist = manhatton_distance((point, sensor))
            sb_dist = manhatton_distance((sensor, beacon))
            if pdist <= sb_dist:
                break
        else:
            print(point)
            tuning_freq = point[0] * 4_000_000 + point[1]
            print(f"Part 2: {tuning_freq}")
            break


if __name__ == "__main__":
    main()
