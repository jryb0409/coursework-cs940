"""Regression checks for the Trie and Network index fixes."""
from trie import Trie
from network import Network


def test_trie_unique_deterministic_prefix_results():
    trie = Trie()
    first, second = [], []
    trie.insert("data structures", first)
    trie.insert("database", second)
    trie.insert("data analytics", first)
    assert trie.search_by_prefix("dat") == [first, second]
    assert trie.search_by_prefix("str") == [first]
    assert trie.search_by_prefix("ruc") == []
    assert trie.search_by_prefix("") == [first, second]


def test_network_station_replacement_updates_name_index():
    class StationStub:
        def __init__(self, station_id, station_name):
            self.station_id = station_id
            self.station_name = station_name

    network = Network()
    old = StationStub("ID1", "Old Place")
    new = StationStub("ID1", "New Road")
    network.add_station(old)
    assert network.search_by_prefix("old") == [old]
    network.add_station(new)
    assert network.get_station("ID1") is new
    assert network.search_by_prefix("old") == []
    assert network.search_by_prefix("new") == [new]
    assert network.search_by_prefix("road") == [new]


if __name__ == "__main__":
    test_trie_unique_deterministic_prefix_results()
    test_network_station_replacement_updates_name_index()
    print("All regression tests passed.")
