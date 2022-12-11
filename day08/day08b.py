import math


def viewing_distance(x_coord: int, y_coord: int, trees: list[list[int]]) -> list[int]:
    curr_tree = trees[x_coord][y_coord]
    x_max = len(trees[0])
    y_max = len(trees)

    # looking north
    north_count: int = 0
    for jn in range(y_coord - 1, -1, -1):
        if jn < 0:
            break
        if trees[x_coord][jn] < curr_tree:
            north_count += 1
        else:
            north_count += 1
            break
    # looking south
    south_count: int = 0
    for js in range(y_coord + 1, y_max + 1):
        if js >= y_max:
            break
        if trees[x_coord][js] < curr_tree:
            south_count += 1
        else:
            south_count += 1
            break
    # looking east
    east_count: int = 0
    for ie in range(x_coord + 1, x_max + 1):
        if ie >= x_max:
            break
        if trees[ie][y_coord] < curr_tree:
            east_count += 1
        else:
            east_count += 1
            break

        # looking west
    west_count: int = 0
    for iw in range(x_coord - 1, -1, -1):
        if iw < 0:
            break
        if trees[iw][y_coord] < curr_tree:
            west_count += 1
        else:
            west_count += 1
            break

    return [north_count, south_count, east_count, west_count]


def main() -> None:
    with open("day08/day08.txt", "r", encoding="UTF-8") as data_file:
        raw = data_file.read()

    trees: list[list[int]] = [[int(x) for x in y] for y in raw.split()]
    visible: list[list[list[int]]] = [[[] for _ in row] for row in trees]

    for y in range(len(trees)):
        for x in range(len(trees[0])):
            visible[x][y] = viewing_distance(x, y, trees)

    max_cell: int = 0
    for line in visible:
        for cell in line:
            prod = math.prod(cell)
            if prod > max_cell:
                max_cell = prod

    print(max_cell)


if __name__ == "__main__":
    main()
