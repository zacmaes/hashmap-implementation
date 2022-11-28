# Name: Zachary Maes
# OSU Email: maesz@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: A6 - Hashmap Implementation
# Due Date: December 2, 2022
# Description: * * * * * * * * * * * * *

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        TODO: Write this implementation
        """
        # use has func to compute initial index
        # if initial index is empty (None or tombstone), insert element
        # else not empty, compute next index with probing sequence, make sure to wraparound if necessary

        # quadratic probing:
        # init_i = original hashed index
        # j = (1, 2, 3, 4, ...)
        # new_i = (init_i + j**2) % capacity

        # -----SC CODE---NEEDS to be modified

        # check load:
        #   if current load factor is >= 0.5:
        #       double capacity (capacity must be prime)
        if self.table_load() >= 0.5:
            double_cap = self._capacity * 2
            self.resize_table(double_cap)

        # hash key with hash function
        # find bucket at hash location
        # replace value or create new key/value at that bucket
        # update size data member

        hash_val = self._hash_function(key)
        initial_index = hash_val % self._capacity
        probe = initial_index
        j = 0
        while self._buckets[probe] is not None and not self._buckets[probe].is_tombstone:
            if self._buckets[probe].key == key:
                self._buckets[probe].value = value
                return
            j += 1
            probe = (initial_index + (j ** 2)) % self._capacity

        if self._buckets[probe] is None or self._buckets[probe].is_tombstone:
            self._buckets[probe] = HashEntry(key, value)
            self._size += 1
        else:
            self._buckets[probe].key = key
            self._buckets[probe].value = value

    def table_load(self) -> float:
        """
        TODO: Write this implementation
        """
        # 𝝺 = n / m
        # 𝝺 Is the load factor
        # n is the total number of elements stored in the table
        # m is the number of buckets

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        TODO: Write this implementation
        """
        count = self._capacity
        for j in range(self._buckets.length()):
            if self._buckets[j] is not None and not self._buckets[j].is_tombstone:
                count -= 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """
        if new_capacity < self._size:
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
        # for j in range(self._capacity):
        #     self._buckets.append(LinkedList())
        for _ in range(self._capacity):
            self._buckets.append(None)

        for r in range(old_data.length()):
            curr_key = old_data[r][0]
            curr_val = old_data[r][1]
            self.put(curr_key, curr_val)

    def get(self, key: str) -> object:
        """
        TODO: Write this implementation
        """
        ret_val = None
        hash_val = self._hash_function(key)
        initial_index = hash_val % self._capacity
        probe = initial_index
        j = 0
        while self._buckets[probe] is not None:
            if self._buckets[probe].key == key and not self._buckets[probe].is_tombstone:
                ret_val = self._buckets[probe].value
                break
            j += 1
            probe = (initial_index + (j ** 2)) % self._capacity

        return ret_val

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """
        hash_val = self._hash_function(key)
        initial_index = hash_val % self._capacity
        probe = initial_index
        j = 0
        while self._buckets[probe] is not None:
            if self._buckets[probe].key == key:
                return True
            j += 1
            probe = (initial_index + (j ** 2)) % self._capacity

        return False

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        hash_val = self._hash_function(key)
        initial_index = hash_val % self._capacity
        probe = initial_index
        j = 0
        while self._buckets[probe] is not None:
            if self._buckets[probe].key == key and not self._buckets[probe].is_tombstone:
                # make tombstone
                # self._buckets[probe].key = None
                # self._buckets[probe].value = None
                self._buckets[probe].is_tombstone = True
                self._size -= 1
                break
            j += 1
            probe = (initial_index + (j ** 2)) % self._capacity

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        array = DynamicArray()
        for i in range(self._buckets.length()):
            if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                key = self._buckets[i].key
                value = self._buckets[i].value
                array.append((key, value))
        return array

    # def __iter__(self):
    #     """
    #     TODO: Write this implementation
    #     """
    #     return HashmapIterator(self)
    #
    # def __next__(self):
    #     """
    #     TODO: Write this implementation
    #     """
    #     pass

    def __iter__(self):
        """
        Create iterator variable self._index for loop

        :return: self
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtains next value and increments iterator variable by 1

        :return: value
        """
        try:
            bucket = self._buckets[self._index]
            while bucket is None or bucket.is_tombstone:
                self._index += 1
                bucket = self._buckets[self._index]

        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return bucket


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        # print(m)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
