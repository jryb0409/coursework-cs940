from exceptions import TrieError

# Represents an individual node in the trie
class _Node:

    __slots__ = ("children", "objects", "object_ids")

    def __init__(self):
        self.children = {}
        self.objects = []
        self.object_ids = set()


class Trie:
    """Word-prefix trie with deterministic, duplicate-free search results."""

    def __init__(self):
        self._root = _Node()
        self._counter = 0
        self._all = []
        self._all_ids = set()

    @staticmethod
    def _validate_key(key):
        if not isinstance(key, str) or not key or key.strip() == "":
            raise TrieError("key must be a non-empty string")
        if key.startswith(" ") or key.endswith(" ") or "  " in key:
            raise TrieError("key contains malformed spacing")

    def insert(self, key: str, obj) -> None:
        self._validate_key(key)

        # Keep a separate list of unique objects in insertion order
        marker = id(obj)
        if marker not in self._all_ids:
            self._all_ids.add(marker)
            self._all.append(obj)

        # Index each word separately, avoiding duplicate objects at shared prefixes
        for word in key.split(" "):
            node = self._root
            for char in word:
                node = node.children.setdefault(char, _Node())
                if marker not in node.object_ids:
                    node.object_ids.add(marker)
                    node.objects.append(obj)

        self._counter += 1

    def search_by_prefix(self, prefix: str) -> list:
        if not isinstance(prefix, str):
            raise TrieError("prefix must be a string")
        if prefix == "":
            return list(self._all)

        node = self._root
        for char in prefix:
            child = node.children.get(char)
            if child is None:
                return []
            node = child

        # Return matching objects in insertion order without scanning other branches
        return list(node.objects)

    def __len__(self):
        return len(self._all)

    def __repr__(self):
        return f"Trie(objects={len(self._all)})"
