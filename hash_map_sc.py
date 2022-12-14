# Name: Zachary Maes
# OSU Email: maesz@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: A6 - Hashmap Implementation
# Due Date: December 2, 2022
# Description:
#   Implementation of a chained hash table and a separate method find_mode(). The hash table has multiple
#   methods including: put(), empty_buckets(), table_load(), clear(), resize_table(), get(), contains_key(), remove(),
#   and get_keys_and_values().


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
        Adds a new key/value pair to the hashmap while checking for load conditions and resizing if necessary.

        :param: key: str
        :param: value: object

        :return: None: modifies hashmap
        """
        # check load:
        #   if current load factor is >= 1.0:
        #       double capacity (capacity must be prime)
        if self.table_load() >= 1.0:
            double_cap = self._capacity * 2
            self.resize_table(double_cap)

        # hash key with hash function
        # find bucket at hash location
        # replace value or create new key/value at that bucket
        # update size data member

        hash_val = self._hash_function(key)
        index = hash_val % self._capacity
        bucket = self._buckets[index]

        node = bucket.contains(key)
        # if bucket has empty linked list, or key does not exist inside bucket:
        if node is None:
            bucket.insert(key, value)
            self._size += 1
        else:
            node.value = value

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hashmap.

        :return: int: number of empty buckets
        """

        count = self._capacity
        for j in range(self._buckets.length()):
            if self._buckets[j].length() > 0:
                count -= 1
        return count

    def table_load(self) -> float:
        """
        Calculates the table load and returns that floating point number. It uses the equation below.

            ???? = n / m
            ???? Is the load factor
            n is the total number of elements stored in the table
            m is the number of buckets

        :return: float: table load
        """

        return self._size / self._capacity

    def clear(self) -> None:
        """
        Empties the hashmap in a simple way.

        :return: None: modifies hashmap
        """
        self._buckets = DynamicArray()

        for j in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hashmap and re-hashes the keys based upon the new capacity passed.

        :param: new_capacity: int

        :return: None: modifies hashmap
        """

        if new_capacity < 1:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # save old keys/values
        old_data = self.get_keys_and_values()

        # set new cap
        self._capacity = new_capacity
        self._size = 0

        # empty old buckets and resize with cap
        self._buckets = DynamicArray()
        for j in range(self._capacity):
            self._buckets.append(LinkedList())

        for r in range(old_data.length()):
            curr_key = old_data[r][0]
            curr_val = old_data[r][1]
            self.put(curr_key, curr_val)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the passed key param.

        :param: key: str

        :return: object: value in hashmap associated with key
        """
        ret_val = None
        for i in range(self._buckets.length()):
            if self._buckets[i].contains(key) is not None:
                ret_val = self._buckets[i].contains(key).value
        return ret_val

    def contains_key(self, key: str) -> bool:
        """
        Returns a bool of T or F if the key is in found inside the map.

        :param: key: str

        :return: bool: True if key in map, False if key not in map
        """
        for i in range(self._buckets.length()):
            if self._buckets[i].contains(key) is not None:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key/value pair from the hashmap.

        :param: key: str

        :return: None: modifies map in place
        """
        for i in range(self._buckets.length()):
            if self._buckets[i].contains(key) is not None:
                self._buckets[i].remove(key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array of tuples containing all of the key/value pairs.

        :return: DynamicArray: array of tuples [(key, value)]
        """
        array = DynamicArray()
        for i in range(self._buckets.length()):
            for node in self._buckets[i]:
                array.append((node.key, node.value))
        return array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Uses a hashmap implementation to find the mode(s) within a passed dynamic array.

    :param: da: DynamicArray

    :return: tuple: (DynamicArray, int) of the mode or modes and the frequency of them.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    for index in range(da.length()):
        # get the current freq of the current key
        key = da[index]
        curr_map_value = map.get(key)

        # if map.get() returns None, that means this key has not yet been entered, make it 0
        if curr_map_value is None:
            curr_map_value = 0

        # enter key with new freq of that key
        new_map_value = curr_map_value + 1
        map.put(key, new_map_value)

        # mode_array_length = mode_array.length()
        #
        # # handle return values
        # if new_map_value > frequency:
        #     # replace all returns
        #     # make frequency match new_map_value
        # elif new_map_value == frequency:

    keys_and_freqs = map.get_keys_and_values()
    mode_array = DynamicArray()
    frequency = 0

    for i in range(keys_and_freqs.length()):
        curr_key = keys_and_freqs[i][0]
        curr_freq = keys_and_freqs[i][1]
        if curr_freq > frequency:
            mode_array = DynamicArray()
            mode_array.append(curr_key)
            frequency = curr_freq
        elif curr_freq == frequency:
            mode_array.append(curr_key)

    return mode_array, frequency


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
    # print(m)
    # print("====================")

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
