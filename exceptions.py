class TubeError(Exception):
    """Base class for Tube-network errors."""

class DataStructureError(Exception):
    """Base class for data-structure errors."""

class InvalidStationDataError(TubeError):
    pass

class UnknownLineError(TubeError):
    pass

class UnknownStationError(TubeError):
    pass

class InvalidPredictionError(TubeError):
    pass

class BranchAlreadyExistsError(TubeError):
    pass

class BranchNotFoundError(TubeError):
    pass

class HeapError(DataStructureError):
    pass

class TrieError(DataStructureError):
    pass
    
class BranchError(TubeError):
    pass
