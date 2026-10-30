
import threading
import hashlib


class CuckooHashTable:
    def __init__(self, size=11):
        self.size = size
        self.table1 = [None] * size
        self.table2 = [None] * size
        self.lock = threading.RLock()

    def _hash(self, key, salt):
        data = f"{salt}:{key}".encode()
        value = int.from_bytes(
            hashlib.sha256(data).digest()[:8], "big"
        )
        return value % self.size

    def h1(self, key):
        return self._hash(key, "first")

    def h2(self, key):
        return self._hash(key, "second")

    def _items(self):
        return [
            key for key in self.table1 + self.table2
            if key is not None
        ]

    def _place(self, key):
        current = key
        table_no = 1
        seen = set()
        max_kicks = 2 * self.size

        for _ in range(max_kicks):
            state = (current, table_no)

            if state in seen:
                return False
            seen.add(state)

            if table_no == 1:
                index = self.h1(current)
                table = self.table1
            else:
                index = self.h2(current)
                table = self.table2

            if table[index] is None:
                table[index] = current
                return True

            table[index], current = current, table[index]
            table_no = 2 if table_no == 1 else 1

        return False

    def insert(self, key):
        with self.lock:
            if self.search(key):
                return True

            old1 = self.table1[:]
            old2 = self.table2[:]
            old_size = self.size

            if self._place(key):
                return True

            # Restore the original tables after failed placement.
            self.table1 = old1
            self.table2 = old2

            # Grow and rehash all keys, including the new key.
            items = self._items() + [key]
            new_size = old_size

            for _ in range(20):
                new_size = new_size * 2 + 1
                self.size = new_size
                self.table1 = [None] * new_size
                self.table2 = [None] * new_size

                if all(self._place(item) for item in items):
                    return True

            # Restore original state if resizing still fails.
            self.size = old_size
            self.table1 = old1
            self.table2 = old2
            return False

    def search(self, key):
        with self.lock:
            return (
                self.table1[self.h1(key)] == key
                or self.table2[self.h2(key)] == key
            )

    def delete(self, key):
        with self.lock:
            i = self.h1(key)
            if self.table1[i] == key:
                self.table1[i] = None
                return True

            i = self.h2(key)
            if self.table2[i] == key:
                self.table2[i] = None
                return True

            return False

    def display(self):
        with self.lock:
            print("Table 1:", self.table1)
            print("Table 2:", self.table2)
            print("Capacity:", self.size)


def worker(table, keys):
    for key in keys:
        if not table.insert(key):
            print("Insertion failed:", key)


if __name__ == "__main__":
    cuckoo = CuckooHashTable()

    # Change these keys for a different test case.
    keys1 = [10, 30, 50]
    keys2 = [20, 40, 60]

    t1 = threading.Thread(target=worker, args=(cuckoo, keys1))
    t2 = threading.Thread(target=worker, args=(cuckoo, keys2))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    cuckoo.display()

    print("Search 30:", cuckoo.search(30))
    print("Delete 30:", cuckoo.delete(30))
    print("Search 30 after deletion:", cuckoo.search(30))
