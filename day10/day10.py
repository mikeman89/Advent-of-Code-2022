from dataclasses import dataclass


@dataclass
class Program:
    cycle: int = 0
    x_val: int = 1
    sprite: tuple[int, int, int] = (0, 1, 2)
    position: int = 0
    drawing: str = ""

    def __post_init__(self):
        self.history: list[tuple[int, int]] = [(self.cycle, self.x_val)]

    def add_to_history(self) -> None:
        self.history.append((self.cycle, self.x_val))

    def noop_command(self) -> None:
        self.cycle += 1
        self.draw()
        self.position += 1
        self.add_to_history()

    def add_x(self, amount: int) -> None:
        self.noop_command()
        self.cycle += 1
        self.draw()
        self.position += 1
        self.add_to_history()
        self.x_val += amount
        self.sprite = (self.x_val - 1, self.x_val, self.x_val + 1)

    def draw(self) -> None:
        if self.position % 40 == 0:
            self.drawing = self.drawing + "\n"
            self.position = 0
        if self.position in self.sprite:
            self.drawing = self.drawing + "#"
        else:
            self.drawing = self.drawing + "."


def parse(raw: str) -> list[list[str]]:
    lines = raw.split("\n")
    instructions: list[list[str]] = []
    for line in lines:
        instructions.append(line.split(" "))
    return instructions


def main() -> None:
    with open("day10/day10.txt", "r", encoding="UTF-8") as file_data:
        raw = file_data.read()
    instructions = parse(raw)
    program = Program()
    for instruction in instructions:
        match instruction[0]:
            case "noop":
                program.noop_command()
            case "addx":
                program.add_x(int(instruction[1]))
            case _:
                print(instruction)
                raise ValueError("Instruction not accounted for")

    signal_strength: int = 0
    for cycle, signal in program.history:
        match cycle:
            case 20:
                signal_strength += cycle * signal
            case 60:
                signal_strength += cycle * signal
            case 100:
                signal_strength += cycle * signal
            case 140:
                signal_strength += cycle * signal
            case 180:
                signal_strength += cycle * signal
            case 220:
                signal_strength += cycle * signal
            case _:
                pass
    print(program.drawing)


if __name__ == "__main__":
    main()
