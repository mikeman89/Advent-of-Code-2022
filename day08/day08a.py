from dataclasses import dataclass


@dataclass
class Tree:
    x: int
    y: int
    size: int


Forest = list[Tree]


def visible_above(tree: Tree, forest: Forest) -> bool:
    for wood in forest:
        if wood.x == tree.x:
            if wood.y > tree.y:
                if wood.size >= tree.size:
                    return False
    return True


def visible_below(tree: Tree, forest: Forest) -> bool:
    for wood in forest:
        if wood.x == tree.x:
            if wood.y < tree.y:
                if wood.size >= tree.size:
                    return False
    return True


def visible_left(tree: Tree, forest: Forest) -> bool:
    for wood in forest:
        if wood.y == tree.y:
            if wood.x < tree.x:
                if wood.size >= tree.size:
                    return False
    return True


def visible_right(tree: Tree, forest: Forest) -> bool:
    for wood in forest:
        if wood.y == tree.y:
            if wood.x > tree.x:
                if wood.size >= tree.size:
                    return False
    return True


def is_visible(
    tree: Tree, forest: Forest, x_min: int, x_max: int, y_min: int, y_max: int
) -> bool:
    if (tree.x == x_min) or (tree.x == x_max) or (tree.y == y_min) or (tree.y == y_max):
        return True
    if (
        not visible_above(tree, forest)
        and not visible_below(tree, forest)
        and not visible_left(tree, forest)
        and not visible_right(tree, forest)
    ):
        return False
    return True


def parse(raw: str) -> Forest:
    forest: Forest = []
    for j, line in enumerate(raw.split("\n")):
        for i, tree in enumerate(line):
            forest.append(Tree(i, j, int(tree)))
    return forest


def get_min_max(forest: Forest) -> tuple[int, int, int, int]:
    x_min: int = 0
    x_max: int = 0
    y_min: int = 0
    y_max: int = 0
    for tree in forest:
        if tree.x > x_max:
            x_max = tree.x
        if tree.x < x_min:
            x_min = tree.x
        if tree.y > y_max:
            y_max = tree.y
        if tree.y < y_min:
            y_min = tree.y
    return (x_min, x_max, y_min, y_max)


def main() -> None:
    with open("day08/day08.txt", "r", encoding="UTF-8") as data_file:
        raw = data_file.read()

    forest = parse(raw)
    x_min, x_max, y_min, y_max = get_min_max(forest)
    count_visible = 0
    for tree in forest:
        if is_visible(tree, forest, x_min, x_max, y_min, y_max):
            count_visible += 1

    print(count_visible)


if __name__ == "__main__":
    main()
