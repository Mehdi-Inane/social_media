import hashlib


def hashFunction(x):
    h = hashlib.sha256(x)  # we'll use sha256 just for this example
    return int(h.hexdigest(), base=16)

class HashTable:
	def __init__(self, size = 11):
		self.size = size
		self.slots = [None] * self.size
		self.data = [None] * self.size
	def hashfunction(self, key, size):
		return key % size
	def rehash(self, oldhash, size):
		return (oldhash + 1) % size
	def put(self, key, data):
		hashvalue = self.hashfunction(key,self.size)
		if self.slots[hashvalue] == None:
			self.slots[hashvalue] = key
			self.data[hashvalue] = data
		else:
			if self.slots[hashvalue] == key:
				self.data[hashvalue] = data  # replace
			else:
				nextslot = self.rehash(hashvalue, len(self.slots))
				while self.slots[nextslot] != None and self.slots[nextslot] != key:
					nextslot = self.rehash(nextslot, len(self.slots))
				if self.slots[nextslot] == None:
					self.slots[nextslot] = key
					self.data[nextslot] = data
				else:
					self.data[nextslot] = data  # replace

	def get(self, key):
		startslot = self.hashfunction(key, len(self.slots))

		data = None
		stop = False
		found = False
		position = startslot
		while self.slots[position] != None and  not found and not stop:
			if self.slots[position] == key:
				found = True
				data = self.data[position]
			else:
				position = self.rehash(position, len(self.slots))
				if position == startslot:
					stop = True
		return data

	def __getitem__(self, key):
		return self.get(key)

	def __setitem__(self, key, data):
		self.put(key, data)
class BloomFilter:
	def __init__(self, m, k, hashFun):
		self.m = m
		self.vector = [0] * m
		self.k = k
		self.data = {}
		self.falsePositive = 0
		self.hashing = hashFun

    # Applying the k hashing functions on the key and getting the corresponding indices
	def get_index_values(self,key):
		hashed_values = []
		for num in range(self.k):
			hashed_values.append(self.hashing((str(key) + str(num)).encode()))
		return [value % self.m for value in hashed_values]
        

	def insert(self, key, value):
		ix = self.get_index_values(key)
		for elem in ix:
			self.vector[elem] = 1
		self.data[key] = value

	def contains(self, key):
		ix = self.get_index_values(key)
		for elem in ix:
			if self.vector[elem] != 1:
				return False
		return True

	def get(self, key):
		if self.contains(key):
			if key in self.data.keys():
				return self.data[key]
			else:
				raise KeyError("No element with this key")
		else:
				print("we here")
				raise KeyError("No element with this key")