from exceptions import InvalidPredictionError

class Prediction:
    def __init__(self, vehicle_id: str, naptan_id: str, line_id: str,
                 platform_name: str, destination_id: str,
                 time_to_station: int, current_location: str):
        if not isinstance(time_to_station, int) or time_to_station < 0:
            raise InvalidPredictionError("time_to_station must be a non-negative integer")
        self.vehicle_id = str(vehicle_id)
        self.naptan_id = str(naptan_id)
        self.line_id = str(line_id)
        self.platform_name = str(platform_name)
        self.destination_id = str(destination_id)
        self.time_to_station = time_to_station
        self.current_location = str(current_location)

    def __lt__(self, other):
        if not isinstance(other, Prediction):
            return NotImplemented
        return (self.time_to_station, self.vehicle_id) < (
            other.time_to_station, other.vehicle_id
        )

    def __repr__(self):
        return (f"Prediction(vehicle={self.vehicle_id!r}, station={self.naptan_id!r}, "
                f"line={self.line_id!r}, in={self.time_to_station}s)")
