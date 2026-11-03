from exceptions import BranchAlreadyExistsError, BranchNotFoundError

class Line:
    def __init__(self, line_id: str, line_name: str):
        self.line_id = line_id
        self.line_name = line_name
        self.branches = {}

    def add_branch(self, branch):
        if branch.branch_id in self.branches:
            raise BranchAlreadyExistsError(f"Branch {branch.branch_id} already exists")
        self.branches[branch.branch_id] = branch

    def get_branch(self, id: int):
        try:
            return self.branches[id]
        except KeyError:
            raise BranchNotFoundError(f"Unknown branch ID: {id}") from None

    def get_stations(self) -> set[str]:
        return {station for branch in self.branches.values() for station in branch}

    def __iter__(self):
        return iter(self.get_stations())

    def __len__(self):
        return len(self.get_stations())

    def __contains__(self, station):
        return station in self.get_stations()

    def __repr__(self):
        return f"Line({self.line_id!r}, {self.line_name!r}, branches={len(self.branches)})"
