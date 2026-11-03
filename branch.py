from exceptions import InvalidStationDataError

class Branch:
    def __init__(self, branch_id: int, next_branch_ids: list[int]):
        if not isinstance(branch_id, int):
            raise InvalidStationDataError("branch_id must be an integer")
        if not isinstance(next_branch_ids, list) or not all(
            isinstance(x, int) for x in next_branch_ids
        ):
            raise InvalidStationDataError("next_branch_ids must be a list of integers")
        self.branch_id = branch_id
        self.next_branch_ids = list(next_branch_ids)
        self.stations: list[str] = []

    def add_station(self, station: str):
        if not isinstance(station, str) or not station:
            raise InvalidStationDataError("station must be a non-empty station ID")
        self.stations.append(station)

    def station_edges(self) -> list[tuple[str, str]]:
        return list(zip(self.stations, self.stations[1:]))

    def branch_edges(self) -> list[tuple[int, int]]:
        return [(self.branch_id, nxt) for nxt in self.next_branch_ids]

    def __iter__(self):
        return iter(self.stations)

    def __len__(self):
        return len(self.stations)

    def __contains__(self, station):
        return station in self.stations

    def __getitem__(self, index):
        try:
            return self.stations[index]
        except (IndexError, TypeError):
            from exceptions import DataStructureError
            raise DataStructureError(f"Invalid station index: {index!r}") from None

    def __repr__(self):
        return f"Branch(id={self.branch_id}, stations={self.stations!r})"
