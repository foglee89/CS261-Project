# Name: Erik Fogle
# OSU Email: Foglee@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 12/3/21
# Description: Program is an implementation of a Hash Map and core methods for interaction.
#               Implemented with Dynamic Array and a Linked List for managing collisions.
#               Two has functions are provided as well as the base code for the Dynamic
#               Array and Linked List structures.

#               NOTE: Class data members are all NOT marked private for direct access. This
#                       does not include the supporting classes LinkedList and DynamicArray;
#                       their data members are not allowed to be directly accessed.


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Description:
            Method takes no parameters and clears the contents of the hash map. It doesn't alter
            the current hash table capacity.

        Parameters:
            None

        Returns:
            None

        """

        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(LinkedList())

        self.size = 0

    def get(self, key: str) -> object:
        """
        Description:
            Method takes a passed key value and returns the associated value that's currently stored
            in the hash map. If the key is not in the has map, the method returns None.

        Parameters:
            key (str):
                passed key value to locate associated value stored in hash map.

        Returns:
            value (obj):
                value in hash map associated with passed key.

        """

        hashed_key = self.hash_function(key) % self.capacity

        bucket = self.buckets[hashed_key]

        node = bucket.contains(key)

        if node is not None:
            return node.value
        else:
            return None

    def put(self, key: str, value: object) -> None:
        """
        Description:
            Method takes a key and a value as parameters and updates the hash map accordingly. If
            the key already exists, the value is updated. If the passed key is new, a new key/value
            pair is added.

        Parameters:
            key (str):
                passed key value associated with the passed value.

            value (obj):
                passed object value associated with the passed key.

        Returns:
            None

        """

        hashed_key = self.hash_function(key) % self.capacity

        bucket = self.buckets[hashed_key]

        node = bucket.contains(key)

        if node is not None:
            node.value = value
        else:
            bucket.insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Description:
            Method takes a passed key value and removes the key/value pair currently stored in the
            hash map. If the key is not in the has map, nothing happens (no exceptions raised).

        Parameters:
            key (str):
                passed key value to locate associated value stored in hash map.

        Returns:
            None

        """

        hashed_key = self.hash_function(key) % self.capacity

        bucket = self.buckets[hashed_key]

        remove = bucket.remove(key)
        if remove is True:
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Description:
            Method takes a key value as a parameter and checks if the key is already in the hash
            map. If the key is already in the hash map, it returns True. Otherwise it returns False;
            including if the hash map is empty (i.e. no keys included).

        Parameters:
            key (str):
                passed key value to check if in hash map.

        Returns:
            None

        """

        hashed_key = self.hash_function(key) % self.capacity

        bucket = self.buckets[hashed_key]

        node = bucket.contains(key)

        if node is not None:
            return True
        else:
            return False

    def empty_buckets(self) -> int:
        """
        Description:
            Method takes no parameters and returns the number of empty buckets in the hash table.

        Parameters:
            None

        Returns:
            emp_buckets (int):
                integer value of the number of empty buckets in the hash table.

        """
        empty_count = 0

        for hashed_key in range(self.capacity):
            current_bucket = self.buckets.get_at_index(hashed_key)
            if current_bucket.length() == 0:
                empty_count += 1

        return empty_count

    def table_load(self) -> float:
        """
        Description:
            Method takes no parameters, calculates the current hash table load factor, and returns
            the value.

        Parameters:
            None

        Returns:
            load_factor (float):
                current decimal value of the hash table's load factor.

        """
        load_factor = self.size / self.capacity
        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        Description:
            Method takes a new capacity value as a parameter and resizes the internal hash table's
            capacity to it. If the new capacity is less than 1, the method does nothing. All existing
            key/value pairs remain in the new hash map and all hash tables links are rehashed.

        Parameters:
            new_capacity (int):
                integer value of the new capacity of the internal hash table.

        Returns:
            None

        """

        if new_capacity < 1:
            return

        self.size = 0

        new_DA = DynamicArray()
        for _ in range(new_capacity):
            new_DA.append(LinkedList())

        for bucket in range(self.capacity):
            current_bucket = self.buckets.pop()
            for node in current_bucket:
                key = node.key
                value = node.value

                hashed_key = self.hash_function(key) % new_capacity
                bucket = new_DA[hashed_key]

                bucket.insert(key, value)
                self.size += 1

        self.buckets = new_DA
        self.capacity = new_capacity

    def get_keys(self) -> DynamicArray:
        """
        Description:
            Method takes no parameters and returns a Dynamic Array of all the keys stored in the hash
            map. The returned Dynamic Array does not have any specified order or sorting.

        Parameters:
            None

        Returns:
            keys (DA):
                Dynamic Array of the keys in the hash map. Not ordered or sorted.

        """

        keys = DynamicArray()

        for hashed_key in range(self.capacity):
            current_bucket = self.buckets.get_at_index(hashed_key)
            for node in current_bucket:
                keys.append(node.key)

        return keys


# BASIC TESTING PROVIDED
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
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
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
