from exceptions import HeapError


class Heap:
    """Stable binary min-heap. Each entry is (key, insertion_counter, object)."""

    # Initialise an empty heap and an insertion counter
    def __init__(self):
        self._data = []
        self._counter = 0

    # Compare two heap entries using their key and insertion order
    @staticmethod
    def _less(a, b):
        return (a[0], a[1]) < (b[0], b[1])

    # Add a new object to the heap while maintaining the heap structure
    def push(self, key, obj):
        entry = (key, self._counter, obj)
        self._counter += 1
        self._data.append(entry)

        # Move the new entry upwards until the heap property is restored
        i = len(self._data) - 1
        while i > 0:
            parent = (i - 1) // 2
            if not self._less(self._data[i], self._data[parent]):
                break
            self._data[i], self._data[parent] = self._data[parent], self._data[i]
            i = parent

    # Remove and return the smallest entry from the heap
    def _remove_min_entry(self):
        if not self._data:
            raise HeapError("Heap is empty")

        minimum = self._data[0]
        last = self._data.pop()

        # Move the last entry to the root and restore the heap structure
        if self._data:
            self._data[0] = last
            i = 0
            n = len(self._data)

            # Move the entry down to its correct position
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

    # Remove and return the object with the smallest key
    def pop(self):
        return self._remove_min_entry()[2]

    # Return the object with the smallest key without removing it
    def peek(self):
        if not self._data:
            raise HeapError("Heap is empty")
        return self._data[0][2]

    # Return the k objects with the smallest keys
    def ksmallest(self, k: int):
        # Validate the requested number of smallest objects
        if not isinstance(k, int) or k < -1:
            raise HeapError("k must be -1 or a non-negative integer")

        if k == 0 or not self._data:
            return []

        # Determine how many objects should be returned
        limit = len(self._data) if k == -1 else min(k, len(self._data))

        # Create a separate min-heap to store candidate entries
        # Each candidate contains its key, insertion order and index
        frontier = []

        # Add a candidate to the frontier while maintaining heap order
        def candidate_push(entry):
            frontier.append(entry)
            i = len(frontier) - 1

            while i > 0:
                parent = (i - 1) // 2
                if frontier[parent][:2] <= frontier[i][:2]:
                    break
                frontier[parent], frontier[i] = frontier[i], frontier[parent]
                i = parent

        # Remove and return the smallest candidate from the frontier
        def candidate_pop():
            result = frontier[0]
            last = frontier.pop()

            # Restore the frontier heap after removing the smallest entry
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

        # Start the candidate heap with the root of the original heap
        root = self._data[0]
        candidate_push((root[0], root[1], 0))

        result = []

        # Repeatedly select the smallest candidate and add its children
        for _ in range(limit):
            if not frontier:
                break

            _, _, index = candidate_pop()
            result.append(self._data[index][2])

            # Add the selected entry's children as new candidates
            for child in (2 * index + 1, 2 * index + 2):
                if child < len(self._data):
                    item = self._data[child]
                    candidate_push((item[0], item[1], child))

        return result

    # Create a heap from an existing collection of key-object pairs
    @classmethod
    def heapify(cls, items):
        heap = cls()

        # Assign insertion order to each item
        heap._data = [(key, i, obj) for i, (key, obj) in enumerate(items)]
        heap._counter = len(heap._data)
        n = len(heap._data)

        # Restore heap order starting from the last parent node
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

    # Return the number of entries in the heap
    def __len__(self):
        return len(self._data)

    # Check whether the heap contains any entries
    def __bool__(self):
        return bool(self._data)

    # Return a readable representation of the heap
    def __repr__(self):
        return f"Heap(size={len(self._data)})"
