from exceptions import TrieError

<<<<<<< HEAD
class _Node:
    __slots__ = ("children", "objects")
    def __init__(self):
        self.children = {}
        self.objects = []  # (insertion_order, object)

class Trie:
    """Prefix trie. Every word is indexed independently; result order is insertion order."""
=======

class _Node:
    """One character node in the prefix trie.

    ``objects`` contains unique objects in first-insertion order. ``object_ids``
    makes duplicate detection an expected O(1) operation without requiring
    stored objects to be hashable.
    """
    __slots__ = ("children", "objects", "object_ids")

    def __init__(self):
        self.children = {}
        self.objects = []
        self.object_ids = set()


class Trie:
    """Word-prefix trie with deterministic, duplicate-free search results."""

>>>>>>> 488def9 (Updated Code)
    def __init__(self):
        self._root = _Node()
        self._counter = 0
        self._all = []
<<<<<<< HEAD
=======
        self._all_ids = set()
>>>>>>> 488def9 (Updated Code)

    @staticmethod
    def _validate_key(key):
        if not isinstance(key, str) or not key or key.strip() == "":
            raise TrieError("key must be a non-empty string")
        if key.startswith(" ") or key.endswith(" ") or "  " in key:
            raise TrieError("key contains malformed spacing")

<<<<<<< HEAD
    def insert(self, key: str, obj):
        self._validate_key(key)
        order = self._counter
        self._counter += 1
        self._all.append((order, obj))
=======
    def insert(self, key: str, obj) -> None:
        self._validate_key(key)

        # The empty-prefix result contains each object only once, in the order
        # in which it was first inserted into this trie.
        marker = id(obj)
        if marker not in self._all_ids:
            self._all_ids.add(marker)
            self._all.append(obj)

        # Index every word independently. Each node records an object only
        # once, even when multiple words/keys belonging to it share a prefix.
>>>>>>> 488def9 (Updated Code)
        for word in key.split(" "):
            node = self._root
            for char in word:
                node = node.children.setdefault(char, _Node())
<<<<<<< HEAD
                node.objects.append((order, obj))

    def search_by_prefix(self, prefix: str):
        if not isinstance(prefix, str):
            raise TrieError("prefix must be a string")
        if prefix == "":
            candidates = self._all
        else:
            node = self._root
            for char in prefix:
                if char not in node.children:
                    return []
                node = node.children[char]
            candidates = node.objects
        # An object may be indexed via multiple words. Use identity so unhashable
        # objects are supported and distinct equal-valued objects are not conflated.
        seen = set()
        result = []
        for _, obj in sorted(candidates, key=lambda item: item[0]):
            marker = id(obj)
            if marker not in seen:
                seen.add(marker)
                result.append(obj)
        return result
=======
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

        # Objects are already unique and in deterministic first-insertion
        # order. No sorting or scan of unrelated trie branches is required.
        return list(node.objects)
>>>>>>> 488def9 (Updated Code)

    def __len__(self):
        return len(self._all)

    def __repr__(self):
        return f"Trie(objects={len(self._all)})"
