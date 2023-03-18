# Name: Cassandra Kramer
# OSU Email: kramecas@oregonstate.edu
# Course: CS261 - Data Structures/ Section 405
# Assignment:6
# Due Date: 3/17/2023
# Description: Use a dynamic array to store a hash table and implement chaining for collision
# resolution


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        new_hash = self._hash_function(key)
        hash_index = new_hash % self._capacity

        if self._buckets[hash_index].length() == 0:
            self._buckets[hash_index].insert(key, value)
            self._size += 1

        elif self._buckets[hash_index] != 0:
            if self._buckets[hash_index].contains(key) is not None:
                node = self._buckets[hash_index].contains(key)
                node.value = value

            else:
                self._buckets[hash_index].insert(key, value)
                self._size += 1
    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets
        """
        buckets = 0
        for index in range(self._buckets.length()):
            if self._buckets[index].length() == 0:
                buckets += 1

        return buckets

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        load_factor = self._size / self._capacity
        return load_factor

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        """
        some_buckets = DynamicArray()
        for index in range(self._capacity):
            some_buckets.append(LinkedList())
        self._buckets = some_buckets
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table
        """
        if new_capacity < 1.0:
            return

        hash_capacity = new_capacity

        if self._is_prime(new_capacity) is False:
            hash_capacity = self._next_prime(new_capacity)

        new_hash = HashMap(hash_capacity, self._hash_function)
        new_buckets = DynamicArray()

        for index in range(hash_capacity):
            new_buckets.append(LinkedList())

        self._size = 0

        for index in range(self._capacity):
            num = self._buckets[index]
            if num.length() != 0:
                for index in num:
                    # new_hash.put(num.key, num.value)
                    new_hash = self._hash_function(index.key)
                    hash_index = new_hash % hash_capacity
                    new_buckets[hash_index].insert(index.key, index.value)

        self._capacity = hash_capacity
        self._buckets = new_buckets


    def get(self, key: str):
        """
        Returns the value associated with the given key
        """
        new_hash = self._hash_function(key)
        hash_index = new_hash % self._capacity

        num = self._buckets[hash_index]
        if num.length() > 0:
            hash_node = num.contains(key)
            if hash_node is not None:
                return hash_node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, or otherwise returns False
        """
        if self.get(key) is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and associated value
        """
        new_hash = self._hash_function(key)
        hash_index = new_hash % self._capacity

        num = self._buckets[hash_index]
        if num.length() > 0:
            node = num.contains(key)
            if node is not None:
                num.remove(key)
                self._size -= 1
            else:
                return None

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map
        """
        new_buckets = DynamicArray()

        for index in range(self._capacity):
            num = self._buckets[index]
            if num.length() > 0:

                for index in num:
                    new_tuple = tuple((index.key, index.value))
                    new_buckets.append(new_tuple)
        return new_buckets
def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives a dynamic array and returns a tuple containing mode, and how many times it occurs
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap

    map = HashMap()
    map._buckets = da

    new_buckets = DynamicArray()

    count = 1
    frequency = 0

    for index in range(map.get_size()):
        num = map._buckets[index]
        mode = num

        for index in range(index + 1, map._buckets.length()):
            if map._buckets[index] == mode:
                count += 1


        if count > frequency:
            some_buckets = DynamicArray()
            new_buckets = some_buckets
            new_buckets._size = 0
            new_buckets.append(mode)
            new_buckets._size += 1
            frequency = count

        elif count == frequency:
            for index in range(new_buckets.length()):
                if new_buckets[index] != mode:
                    index += 1
                    if index > new_buckets.length() - 1:
                        new_buckets.append(mode)
                        new_buckets._size += 1


        count = 1


    return new_buckets, frequency



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
