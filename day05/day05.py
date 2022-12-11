import re


def parse_stack_moves(raw: str) -> tuple[str, str]:
    stack, moves = raw.split("\n\n")
    return stack, moves


def clean_stacks(stacks: str) -> list[str]:
    cleaned = (
        stacks.replace("    ", "*").replace(" ", "").replace("[", "").replace("]", "")
    )
    cleaned_stacks = cleaned.split("\n")
    return cleaned_stacks


def build_stacks_lists(cleaned_stacks: list[str]) -> list[list[str]]:
    stack_lists: list[list[str]] = []
    num_stacked = int(cleaned_stacks[-1][-1])
    for _ in range(num_stacked):
        stack_lists.append([])
    for stack in reversed(cleaned_stacks[:-1]):
        for i, crate in enumerate(stack):
            if crate == "*":
                continue
            stack_lists[i].append(crate)
    return stack_lists


def clean_move_list(moves: str) -> list[list[int]]:
    move_list: list[list[int]] = []
    moves_uncleaned = moves.split("\n")
    # num_moves = len(moves_uncleaned)
    # for _ in range(num_moves):
    #     move_list.append([])
    for line in moves_uncleaned:
        match = re.findall(r"\d{1,3}", line)
        match = [int(m) for m in match]
        move_list.append(match)
    return move_list


def rearrange_part_1(
    cleaned_stacks: list[list[str]], cleaned_moves: list[list[int]]
) -> list[list[str]]:
    for move in cleaned_moves:
        for _ in range(move[0]):
            crate = cleaned_stacks[move[1] - 1].pop()
            cleaned_stacks[move[2] - 1].append(crate)
    return cleaned_stacks


def rearrange_part_2(
    cleaned_stacks: list[list[str]], cleaned_moves: list[list[int]]
) -> list[list[str]]:
    for move in cleaned_moves:
        crates = cleaned_stacks[move[1] - 1][-move[0] :]
        for crate in crates:
            cleaned_stacks[move[2] - 1].append(crate)
            cleaned_stacks[move[1] - 1].pop()
    return cleaned_stacks


def top_of_each(cleaned_stacks: list[list[str]]) -> str:
    top_of_stacks: str = ""
    for stack in cleaned_stacks:
        top_of_stacks += stack[-1]
    return top_of_stacks


def main() -> None:
    with open("day05/day05.txt", "r", encoding="UTF-8") as file_data:
        raw_data = file_data.read()
    stacks, moves = parse_stack_moves(raw_data)
    cleaned_stacks = clean_stacks(stacks=stacks)
    stack_lists = build_stacks_lists(cleaned_stacks=cleaned_stacks)
    move_list = clean_move_list(moves=moves)
    final_stacks = rearrange_part_2(stack_lists, move_list)
    print(final_stacks)
    final_output = top_of_each(final_stacks)
    print(final_output)


if __name__ == "__main__":
    main()
