from dataclasses import dataclass

POINTS = {
    "X": 1,
    "Y": 2,
    "Z": 3,
    "Lose": 0,
    "Tie": 3,
    "Win": 6,
}


@dataclass
class RPC:
    opp_choice: str
    my_choice: str

    def find_winner(self) -> str:
        if self.opp_choice == "A":
            if self.my_choice == 'X':
                return 'Tie'
            elif self.my_choice == 'Y':
                return 'Win'
            elif self.my_choice == 'Z':
                return 'Lose'
        elif self.opp_choice == "B":
            if self.my_choice == 'X':
                return 'Lose'
            elif self.my_choice == 'Y':
                return 'Tie'
            elif self.my_choice == 'Z':
                return 'Win'
        elif self.opp_choice == "C":
            if self.my_choice == 'X':
                return 'Win'
            elif self.my_choice == 'Y':
                return 'Lose'
            elif self.my_choice == 'Z':
                return 'Tie'


def parse_data(raw: str) -> list[RPC]:
    rpc = []
    lines = [str(line) for line in raw.split('\n')]
    for text in lines:
        x, y = text.split(sep=' ')
        rpc.append(RPC(x, y))
    return rpc


# def find_winner(rpc: RPC) -> str:
#     if rpc.opp_choice == "A":
#         if rpc.my_choice == 'X':
#             return 'Tie'
#         elif rpc.my_choice == 'Y':
#             return 'Lose'
#         elif rpc.my_choice == 'Z':
#             return 'Win'
#     elif rpc.opp_choice == "B":
#         if rpc.my_choice == 'X':
#             return 'Win'
#         elif rpc.my_choice == 'Y':
#             return 'Tie'
#         elif rpc.my_choice == 'Z':
#             return 'Lose'
#     elif rpc.opp_choice == "C":
#         if rpc.my_choice == 'X':
#             return 'Lose'
#         elif rpc.my_choice == 'Y':
#             return 'Win'
#         elif rpc.my_choice == 'Z':
#             return 'Tie'


def get_points(rpcs: list[RPC], point_list: dict[str, int]) -> int:
    tot_points = 0
    for rpc in rpcs:
        result = rpc.find_winner()
        tot_points = tot_points + point_list[result] + point_list[rpc.my_choice]
    return tot_points


def main() -> None:
    with open("data02.txt", 'r') as f:
        RAW = f.read()
    games = parse_data(RAW)
    total_points = get_points(games, POINTS)
    print(total_points)


if __name__ == '__main__':
    main()
