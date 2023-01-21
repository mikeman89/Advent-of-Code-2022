# pylint: disable=missing-class-docstring,missing-function-docstring,missing-module-docstring
import heapq
import re
from collections import deque
from dataclasses import dataclass, field
from typing import NamedTuple, Optional

RGX = r"Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z, ]+)"


@dataclass
class Valve:
    name: str
    flow: int
    tunnels: list[str]
    # status: bool = False  # True is open False is closed

    @staticmethod
    def from_string(text: str) -> "Valve":
        res = re.match(RGX, text)
        if res:
            name, flow, tunnels = res.groups()
        else:
            raise ValueError(r"could not parse {s}")

        return Valve(name, int(flow), tunnels.split(", "))


class OQItem(NamedTuple):
    negative_best_possible: int
    loc: str
    elephant_loc: str
    time: int
    etime: int
    released: int
    opened: set[str]
    prev: Optional["OQItem"] = None


# creating the Optimized Network
@dataclass
class ONetwork:
    valves: list[Valve]
    valves_by_name: dict[str, Valve] = field(default_factory=dict)
    distances: dict[str, dict[str, int]] = field(default_factory=dict)
    names: set[str] = field(default_factory=set)

    def __post_init__(self):
        self.valves_by_name = {v.name: v for v in self.valves}
        self.distances = self.compute_distances()
        self.valves = [v for v in self.valves if v.flow > 0]
        self.names = {v.name for v in self.valves}

    def compute_distances(self) -> dict[str, dict[str, int]]:
        distances: dict[str, dict[str, int]] = {}
        for start in self.valves_by_name:
            distances[start] = {}
            q: deque[tuple[int, str]] = deque([(0, start)])
            while q:
                dist, loc = q.popleft()
                if loc in distances[start]:
                    continue
                distances[start][loc] = dist
                for tunnel in self.valves_by_name[loc].tunnels:
                    q.append((dist + 1, tunnel))

        # now clean things up
        for name, dists in distances.items():
            for v in self.valves:
                if v.flow == 0 or v.name == name:
                    del dists[v.name]

        return distances

    @staticmethod
    def from_string(text: str) -> "ONetwork":
        valves = [Valve.from_string(line) for line in text.splitlines()]
        return ONetwork(valves)

    def best_possible(self, so_far: int, remaining_steps: int, open: set[str]) -> int:
        # smallest to largest
        closed_flows = sorted([v.flow for v in self.valves if v.name not in open])

        tot = so_far
        while remaining_steps > 0 and closed_flows:
            # for me
            new_flow = closed_flows.pop()

            # for the elephant
            if closed_flows:
                new_flow += closed_flows.pop()

            tot += new_flow * remaining_steps
            # one to move one to open
            remaining_steps -= 2

        return tot

    def most_pressure(self, num_steps: int = 26, start: str = "AA") -> int:
        best_possible = self.best_possible(0, num_steps, set())
        q = [OQItem(-best_possible, start, start, 0, 0, 0, set())]

        best = -1
        best_qitem = None
        count = 0

        while q:
            qitem = heapq.heappop(q)
            # print(qitem)
            count += 1
            # if count % 100_000 == 0:
            #     print(count)
            #     print(qitem)
            #     print("best", best)
            #     print("q Size", len(q))
            # print()
            # print("popping", qitem)
            nbp, loc, eloc, time, etime, released, open, _ = qitem

            # the best remaining possible is less than something we've already achieved
            if -nbp < best:
                return best
            # new best
            if released > best:
                best = released
                best_qitem = qitem
                # print("new best", best)
                # print(qitem)

            # all open nothing left to do
            if len(open) == len(self.valves):
                continue

            # where i go first if i am earlier than i have to be
            if time <= etime and time < num_steps:
                steps_remaining = num_steps - time
                # move and open
                dists = self.distances[loc]
                for tunnel in set(dists) - open:
                    time_to_move = dists[tunnel]
                    added_flow = (
                        steps_remaining - time_to_move - 1
                    ) * self.valves_by_name[tunnel].flow
                    # print("added_flow", added_flow)
                    new_released = released + added_flow
                    # print("new_released",new_released)
                    new_open = open | {tunnel}
                    new_nbp = -self.best_possible(
                        new_released, steps_remaining - time_to_move - 1, new_open
                    )
                    heapq.heappush(
                        q,
                        OQItem(
                            new_nbp,
                            tunnel,
                            eloc,
                            time + time_to_move + 1,
                            etime,
                            new_released,
                            new_open,
                        ),
                    )

            # where the elephant goes first when it gets there earlier
            if etime <= time and etime < num_steps:
                steps_remaining = num_steps - etime
                # if its open i should move
                dists = self.distances[eloc]
                for tunnel in set(dists) - open:
                    time_to_move = dists[tunnel]
                    added_flow = (
                        steps_remaining - time_to_move - 1
                    ) * self.valves_by_name[tunnel].flow
                    new_released = released + added_flow
                    new_open = open | {tunnel}
                    new_nbp = -self.best_possible(
                        new_released, steps_remaining - time_to_move - 1, new_open
                    )
                    heapq.heappush(
                        q,
                        OQItem(
                            new_nbp,
                            tunnel,
                            eloc,
                            time,
                            etime + time_to_move + 1,
                            new_released,
                            new_open,
                        ),
                    )

        return best


def main() -> None:
    with open("day16/test_day16.txt", "r", encoding="UTF-8") as file_data:
        raw = file_data.read()
    onetwork = ONetwork.from_string(raw)
    best = onetwork.most_pressure(26, "AA")
    print(best)


if __name__ == "__main__":
    main()
