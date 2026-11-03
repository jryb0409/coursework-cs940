from math import radians, sin, cos, asin, sqrt
from exceptions import InvalidStationDataError

TUBE_LINES = {
    "bakerloo", "central", "circle", "district", "hammersmith-city",
    "jubilee", "metropolitan", "northern", "piccadilly", "victoria",
    "waterloo-city"
}

class Station:
    def __init__(self, station_id: str, station_name: str,
                 interchange_lines: list, zones: str, lat: float, lon: float):
        if not isinstance(station_id, str) or not station_id:
            raise InvalidStationDataError("station_id must be a non-empty string")
        if not isinstance(station_name, str) or not station_name:
            raise InvalidStationDataError("station_name must be a non-empty string")
        try:
            latitude, longitude = float(lat), float(lon)
        except (TypeError, ValueError):
            raise InvalidStationDataError("latitude and longitude must be numbers") from None
        if not -90 <= latitude <= 90:
            raise InvalidStationDataError("latitude must be between -90 and 90")
        if not -180 <= longitude <= 180:
            raise InvalidStationDataError("longitude must be between -180 and 180")
        if not isinstance(zones, str):
            raise InvalidStationDataError("zones must be a string")
        if not isinstance(interchange_lines, list):
            raise InvalidStationDataError("interchange_lines must be a list")

        self.station_id = station_id
        self.station_name = station_name
        self.interchange_lines = [
            item["id"] for item in interchange_lines
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]
        self.zones = [z.strip() for z in zones.replace("/", "+").split("+") if z.strip()]
        self.lat = latitude
        self.lon = longitude

    def is_interchange(self) -> bool:
        return len({line for line in self.interchange_lines if line in TUBE_LINES}) > 1

    def distance_to(self, other: "Station") -> float:
        if not isinstance(other, Station):
            raise InvalidStationDataError("distance_to expects another Station")
        lat1, lat2 = radians(self.lat), radians(other.lat)
        dlat = lat2 - lat1
        dlon = radians(other.lon - self.lon)
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        return 2 * 6371.0 * asin(sqrt(min(1.0, a)))

    def __eq__(self, other):
        return isinstance(other, Station) and self.station_id == other.station_id

    def __hash__(self):
        return hash(self.station_id)

    def __repr__(self):
        return (f"Station({self.station_id!r}, {self.station_name!r}, "
                f"zones={self.zones!r})")

    def __str__(self):
        return self.station_name
