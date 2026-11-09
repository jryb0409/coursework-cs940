from math import radians, sin, cos, asin, sqrt
from exceptions import InvalidStationDataError

# List of recognised London Underground lines
TUBE_LINES = {
    "bakerloo", "central", "circle", "district", "hammersmith-city",
    "jubilee", "metropolitan", "northern", "piccadilly", "victoria",
    "waterloo-city"
}


class Station:
    # Initialise a station with its ID, name, lines, zones and coordinates
    def __init__(self, station_id: str, station_name: str,
                 interchange_lines: list, zones: str, lat: float, lon: float):

        # Check that the station ID and name are non-empty strings
        if not isinstance(station_id, str) or not station_id:
            raise InvalidStationDataError("station_id must be a non-empty string")
        if not isinstance(station_name, str) or not station_name:
            raise InvalidStationDataError("station_name must be a non-empty string")

        # Convert latitude and longitude into numbers
        try:
            latitude, longitude = float(lat), float(lon)
        except (TypeError, ValueError):
            raise InvalidStationDataError("latitude and longitude must be numbers") from None

        # Check that the coordinates are within valid geographical ranges
        if not -90 <= latitude <= 90:
            raise InvalidStationDataError("latitude must be between -90 and 90")
        if not -180 <= longitude <= 180:
            raise InvalidStationDataError("longitude must be between -180 and 180")

        # Validate the zones and interchange lines
        if not isinstance(zones, str):
            raise InvalidStationDataError("zones must be a string")
        if not isinstance(interchange_lines, list):
            raise InvalidStationDataError("interchange_lines must be a list")

        # Store the station information
        self.station_id = station_id
        self.station_name = station_name

        # Extract valid line IDs from the interchange line data
        self.interchange_lines = [
            item["id"] for item in interchange_lines
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]

        # Split the zones into a list and remove unnecessary spaces
        self.zones = [z.strip() for z in zones.replace("/", "+").split("+") if z.strip()]
        self.lat = latitude
        self.lon = longitude

    # Check whether the station connects more than one Underground line
    def is_interchange(self) -> bool:
        return len({line for line in self.interchange_lines if line in TUBE_LINES}) > 1

    # Calculate the distance between this station and another station
    def distance_to(self, other: "Station") -> float:
        # Check that the supplied object is another Station
        if not isinstance(other, Station):
            raise InvalidStationDataError("distance_to expects another Station")

        # Convert coordinates from degrees to radians
        lat1, lat2 = radians(self.lat), radians(other.lat)
        dlat = lat2 - lat1
        dlon = radians(other.lon - self.lon)

        # Calculate the distance using the Haversine formula
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        return 2 * 6371.0 * asin(sqrt(min(1.0, a)))

    # Compare two stations using their station IDs
    def __eq__(self, other):
        return isinstance(other, Station) and self.station_id == other.station_id

    # Generate a hash using the station ID
    def __hash__(self):
        return hash(self.station_id)

    # Return a readable representation of the station
    def __repr__(self):
        return (f"Station({self.station_id!r}, {self.station_name!r}, "
                f"zones={self.zones!r})")

    # Return the station name as its string representation
    def __str__(self):
        return self.station_name
