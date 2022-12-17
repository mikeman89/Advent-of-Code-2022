# pylint: disable=missing-class-docstring,missing-function-docstring,missing-module-docstring
import heapq
from dataclasses import dataclass, field
from typing import NamedTuple


@dataclass
class Valve:
    name: str
    flow_rate: int
    tunnels: list[str]
    status: bool = False  # True is open False is closed


class QItem(NamedTuple):
    negative_best_possible: int
    loc: str
    time: int
    released: int
    opened: set[str]
    current_path: list[str]


@dataclass
class Network:
    valves: list[Valve]
    valves_by_name: dict[str, Valve] = field(default_factory=dict)

    def best_possible(self, so_far: int, remaining_steps: int, opened: set[str]) -> int:
        closed_flows = sorted(
            [v.flow_rate for v in self.valves if v.name not in opened]
        )
        tot = so_far
        while remaining_steps > 0 and closed_flows:
            tot += closed_flows.pop() * remaining_steps
            remaining_steps -= 1
        return tot

    def most_pressure(self, num_steps: int = 30, start: str = "AA") -> int:
        valves_with_flow = {v.name for v in self.valves if v.flow_rate > 0}

        best_possible = self.best_possible(0, num_steps, set())
        q = [QItem(-best_possible, start, 0, 0, set(), [])]
        best = -1

        while q:
            nbp, loc, time, released, opened, current_path = heapq.heappop(q)
            steps_remianing = num_steps - time
            # the best remaining possiblity is less than something we have already achieved
            if -nbp < best:
                return best
            # out of time or all good valves are opened
            if time == num_steps or valves_with_flow == opened:
                if released > best:
                    best = released
                continue
            valve = self.valves_by_name[loc]
            if valve.flow_rate > 0 and loc not in opened:
                flow = valve.flow_rate * (steps_remianing - 1)
                bp = self.best_possible(
                    released + flow, steps_remianing - 1, opened | {loc}
                )
                # reset current path when i open a valve
                item = QItem(
                    -bp, loc, time + 1, released + flow, opened | {loc}, current_path=[]
                )
                heapq.heappush(q, item)
            for tunnel in valve.tunnels:
                if tunnel in current_path:
                    # backtracking is a waste of time
                    continue
                bp = self.best_possible(released, steps_remianing - 1, opened)
                current_path = current_path + [tunnel]
                item = QItem(-bp, tunnel, time + 1, released, opened, current_path)
                heapq.heappush(q, item)
        return best


# not nice byt works, should use regex for this and some staticmethods
def parse(lines: list[str]) -> Network:
    valves: list[Valve] = []
    for line in lines:
        words = line.split(" ")
        name = words[1]
        flow = int(words[4].split("=")[1].split(";")[0])
        if "valve" in words:
            direction = [words[-1].strip()]
        else:
            direction = line.split("valves ")[1].strip().split(",")
            for i, direct in enumerate(direction):
                direction[i] = direct.strip()
        valves.append(Valve(name, flow, direction))
    by_name: dict[str, Valve] = {v.name: v for v in valves}
    return Network(valves, by_name)


def main() -> None:
    with open("day16/day16.txt", "r", encoding="UTF-8") as file_data:
        lines = file_data.readlines()
    network = parse(lines)
    print(network.most_pressure(30, "AA"))


if __name__ == "__main__":
    main()
