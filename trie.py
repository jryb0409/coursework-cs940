from exceptions import TrieError

class _Node:
    __slots__ = ("children", "objects")
    def __init__(self):
        self.children = {}
        self.objects = []  # (insertion_order, object)

class Trie:
    """Prefix trie. Every word is indexed independently; result order is insertion order."""
    def __init__(self):
        self._root = _Node()
        self._counter = 0
        self._all = []

    @staticmethod
    def _validate_key(key):
        if not isinstance(key, str) or not key or key.strip() == "":
            raise TrieError("key must be a non-empty string")
        if key.startswith(" ") or key.endswith(" ") or "  " in key:
            raise TrieError("key contains malformed spacing")

    def insert(self, key: str, obj):
        self._validate_key(key)
        order = self._counter
        self._counter += 1
        self._all.append((order, obj))
        for word in key.split(" "):
            node = self._root
            for char in word:
                node = node.children.setdefault(char, _Node())
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

    def __len__(self):
        return len(self._all)

    def __repr__(self):
        return f"Trie(objects={len(self._all)})"
