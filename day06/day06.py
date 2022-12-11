def check_unique(texts: list[str], length: int) -> bool:
    unique = set(texts)
    if len(unique) == length:
        return True
    return False


def pass_data(raw: str, length: int) -> int | None:
    raw_list = list(raw)
    for i in range(len(raw_list)):
        temp = raw_list[i : i + length]
        if check_unique(temp, length):
            return i + length
    return None


def main() -> None:
    with open("day06/day06.txt", "r", encoding="UTF-8") as file_data:
        raw = file_data.read()
    print(pass_data(raw, 14))


if __name__ == "__main__":
    main()
