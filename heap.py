from exceptions import HeapError

class Heap:
    """Stable binary min-heap. Each entry is (key, insertion_counter, object)."""
    def __init__(self):
        self._data = []
        self._counter = 0

    @staticmethod
    def _less(a, b):
        return (a[0], a[1]) < (b[0], b[1])

    def push(self, key, obj):
        entry = (key, self._counter, obj)
        self._counter += 1
        self._data.append(entry)
        i = len(self._data) - 1
        while i > 0:
            parent = (i - 1) // 2
            if not self._less(self._data[i], self._data[parent]):
                break
            self._data[i], self._data[parent] = self._data[parent], self._data[i]
            i = parent

    def _remove_min_entry(self):
        if not self._data:
            raise HeapError("Heap is empty")
        minimum = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            i = 0
            n = len(self._data)
            while True:
                left, right = 2 * i + 1, 2 * i + 2
                smallest = i
                if left < n and self._less(self._data[left], self._data[smallest]):
                    smallest = left
                if right < n and self._less(self._data[right], self._data[smallest]):
                    smallest = right
                if smallest == i:
                    break
                self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
                i = smallest
        return minimum

    def pop(self):
        return self._remove_min_entry()[2]

    def peek(self):
        if not self._data:
            raise HeapError("Heap is empty")
        return self._data[0][2]

    def ksmallest(self, k: int):
        if not isinstance(k, int) or k < -1:
            raise HeapError("k must be -1 or a non-negative integer")
        if k == 0 or not self._data:
            return []
        limit = len(self._data) if k == -1 else min(k, len(self._data))

        # Candidate frontier is itself a binary min-heap of (key, insertion order, index).
        # Only children of a candidate removed from the frontier are added.
        frontier = []

        def candidate_push(entry):
            frontier.append(entry)
            i = len(frontier) - 1
            while i > 0:
                parent = (i - 1) // 2
                if frontier[parent][:2] <= frontier[i][:2]:
                    break
                frontier[parent], frontier[i] = frontier[i], frontier[parent]
                i = parent

        def candidate_pop():
            result = frontier[0]
            last = frontier.pop()
            if frontier:
                frontier[0] = last
                i, n = 0, len(frontier)
                while True:
                    left, right = 2 * i + 1, 2 * i + 2
                    smallest = i
                    if left < n and frontier[left][:2] < frontier[smallest][:2]:
                        smallest = left
                    if right < n and frontier[right][:2] < frontier[smallest][:2]:
                        smallest = right
                    if smallest == i:
                        break
                    frontier[i], frontier[smallest] = frontier[smallest], frontier[i]
                    i = smallest
            return result

        root = self._data[0]
        candidate_push((root[0], root[1], 0))
        result = []
        for _ in range(limit):
            if not frontier:
                break
            _, _, index = candidate_pop()
            result.append(self._data[index][2])
            for child in (2 * index + 1, 2 * index + 2):
                if child < len(self._data):
                    item = self._data[child]
                    candidate_push((item[0], item[1], child))
        return result

    @classmethod
    def heapify(cls, items):
        heap = cls()
        heap._data = [(key, i, obj) for i, (key, obj) in enumerate(items)]
        heap._counter = len(heap._data)
        n = len(heap._data)
        for start in range(n // 2 - 1, -1, -1):
            i = start
            while True:
                left, right = 2 * i + 1, 2 * i + 2
                smallest = i
                if left < n and heap._less(heap._data[left], heap._data[smallest]):
                    smallest = left
                if right < n and heap._less(heap._data[right], heap._data[smallest]):
                    smallest = right
                if smallest == i:
                    break
                heap._data[i], heap._data[smallest] = heap._data[smallest], heap._data[i]
                i = smallest
        return heap

    def __len__(self):
        return len(self._data)

    def __bool__(self):
        return bool(self._data)

    def __repr__(self):
        return f"Heap(size={len(self._data)})"
