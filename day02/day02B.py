from dataclasses import dataclass

POINTS = {
    "X": 0,
    "Y": 3,
    "Z": 6,
    "R": 1,
    "P": 2,
    "S": 3,
}


@dataclass
class RPC:
    opp_choice: str
    decision: str

    def what_choice(self) -> str:
        if self.opp_choice == "A":
            if self.decision == 'X':
                return 'S'
            elif self.decision == 'Y':
                return 'R'
            elif self.decision == 'Z':
                return 'P'
        elif self.opp_choice == "B":
            if self.decision == 'X':
                return 'R'
            elif self.decision == 'Y':
                return 'P'
            elif self.decision == 'Z':
                return 'S'
        elif self.opp_choice == "C":
            if self.decision == 'X':
                return 'P'
            elif self.decision == 'Y':
                return 'S'
            elif self.decision == 'Z':
                return 'R'


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
        result = rpc.what_choice()
        tot_points = tot_points + point_list[result] + point_list[rpc.decision]
    return tot_points


def main() -> None:
    with open("data02.txt", 'r') as f:
        RAW = f.read()
    games = parse_data(RAW)
    total_points = get_points(games, POINTS)
    print(total_points)


if __name__ == '__main__':
    main()
