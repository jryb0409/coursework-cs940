import re
import unicodedata
from exceptions import UnknownLineError, UnknownStationError, InvalidPredictionError
from heap import Heap
from trie import Trie

class Network:
    def __init__(self):
        self.lines = {}
        self.stations = {}
        self._station_trie = Trie()
        self._station_heaps = {}
        self._line_heaps = {}
        self._station_line_heaps = {}
        self._train_heaps = {}

    @staticmethod
    def _normalise(text):
        text = unicodedata.normalize("NFKD", text).casefold()
        text = "".join(ch for ch in text if not unicodedata.combining(ch))
        text = re.sub(r"[^a-z0-9]+", " ", text)
        return " ".join(text.split())

    def add_line(self, line):
        self.lines[line.line_id] = line

    def get_line(self, line_id):
        try:
            return self.lines[line_id]
        except KeyError:
            raise UnknownLineError(f"Unknown line: {line_id}") from None

    def _rebuild_station_trie(self):
        """Rebuild the name index from canonical station records.

        Rebuilding on replacement removes the old name and indexes the new
        name. The station dictionary remains the single source of truth.
        """
        trie = Trie()
        for current_station in self.stations.values():
            normalised = self._normalise(current_station.station_name)
            if normalised:
                trie.insert(normalised, current_station)
        self._station_trie = trie

    def add_station(self, station):
        # Replace by station_id, then rebuild the derived name index. This
        # keeps the trie synchronised even when the station name changes.
        self.stations[station.station_id] = station
        self._rebuild_station_trie()

    def get_station(self, station_id):
        try:
            return self.stations[station_id]
        except KeyError:
            raise UnknownStationError(f"Unknown station: {station_id}") from None

    @staticmethod
    def _add_to_index(index, key, prediction):
        if key not in index:
            index[key] = Heap()
        index[key].push(prediction.time_to_station, prediction)

    def add_prediction(self, prediction):
        station_id, line_id = prediction.naptan_id, prediction.line_id
        train_key = (prediction.vehicle_id, line_id)
        self._add_to_index(self._station_heaps, station_id, prediction)
        self._add_to_index(self._line_heaps, line_id, prediction)
        self._add_to_index(self._station_line_heaps, (station_id, line_id), prediction)
        self._add_to_index(self._train_heaps, train_key, prediction)

    def search_by_prefix(self, prefix):
        if not isinstance(prefix, str):
            return []
        normalised = self._normalise(prefix)
        matches = self._station_trie.search_by_prefix(normalised)
        # The trie is rebuilt from canonical records, so these are current
        # station objects. Deduplicate by station ID as a defensive measure.
        current = {}
        for station in matches:
            current[station.station_id] = self.stations[station.station_id]
        return sorted(current.values(), key=lambda s: s.station_name.casefold())

    @staticmethod
    def _query(index, key, k):
        if not isinstance(k, int) or k < -1:
            raise InvalidPredictionError("k must be -1 or a non-negative integer")
        heap = index.get(key)
        if heap is None or k == 0:
            return []
        return heap.ksmallest(k)

    def next_arrivals_by_station(self, station_id, k):
        self.get_station(station_id)
        return self._query(self._station_heaps, station_id, k)

    def next_arrivals_by_line(self, line_id, k):
        self.get_line(line_id)
        return self._query(self._line_heaps, line_id, k)

    def next_arrivals_by_station_and_line(self, station_id, line_id, k):
        self.get_station(station_id)
        line = self.get_line(line_id)
        if station_id not in line.get_stations():
            raise InvalidPredictionError("The specified line does not serve this station")
        return self._query(self._station_line_heaps, (station_id, line_id), k)

    def next_stations_by_train(self, vehicle_id, line_id, k):
        self.get_line(line_id)
        return self._query(self._train_heaps, (vehicle_id, line_id), k)

    def __repr__(self):
        return f"Network(lines={len(self.lines)}, stations={len(self.stations)})"
