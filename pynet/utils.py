##
# -*- coding: utf-8 -*-
##
import json
import os

class expanded_dict:
	def walk(self, data):
		for k, v in data.items():
			if isinstance(v, dict):
				setattr(self, k, type(self)(v))
			else:
				setattr(self, k, v)

	def __repr__(self):
		return self.data_repr

	def __init__(self, data):
		self.data_repr = data.__repr__()
		self.walk(data)

class json_wrapper:
	__writing__ = True
	__ready__ = False
	__data__ = None

	@property
	def isiterable(self):
		return hasattr(self.__data__, '__iter__')

	@property
	def __type__(self):
		return type(self.__data__)

	def walk_data(self, data):
		for k, v in data.items():
			if isinstance(v, dict):
				data[k] = expanded_dict(v)
			else:
				pass

	def __write__(self):
		ready = object.__getattribute__(self, '__ready__')
		writing = object.__getattribute__(self, '__writing__')
		if ready and writing:
			with open(self.fp, 'w') as inf:
				json.dump(self.__data__, inf)


	def __init__(self, fp, default={}, **kwargs):
		if os.path.exists(fp):
			if not os.path.isfile(fp):
				raise Exception('filepath supplied is already a directory')
		else:
			with open(fp, 'w') as inf:
				json.dump(default, inf)

		self.fp = fp

		with open(fp, 'r') as inf:
			data = json.load(inf)
			self.__data__ = data
			self.walk_data(data)

		self.__ready__ = True

	def __iter__(self):
		return self

	def __next__(self):
		data = object.__getattribute__(self, '__data__')
		counter += 1
		try:
			return data[tuple(data.keys())[counter]]
		except IndexError:
			counter = 0
			raise StopIteration

	def __repr__(self):
		return self.__data__.__repr__()

	def __str__(self):
		return self.__data__.__str__()

	def __getitem__(self, key):
		ready = object.__getattribute__(self, '__ready__')
		data = object.__getattribute__(self, '__data__')
		if ready:
			return data[key]
			object.__getattribute__(self, 'walk_data')(data)
		else:
			return object.__getattribute__(self, key)

	def __getattr__(self, key):
		ready = object.__getattribute__(self, '__ready__')
		data = object.__getattribute__(self, '__data__')
		if ready:
			return data[key]
			object.__getattribute__(self, 'walk_data')(data)
		else:
			return object.__getattribute__(self, key)

	def __setattr__(self, key, value):
		ready = object.__getattribute__(self, '__ready__')
		data = object.__getattribute__(self, '__data__')
		if ready:
			data[key] = value
			object.__getattribute__(self, 'walk_data')(data)
			object.__getattribute__(self, '__write__')()
		else:
			object.__setattr__(self, key, value)

	def __setitem__(self, key, value):
		ready = object.__getattribute__(self, '__ready__')
		data = object.__getattribute__(self, '__data__')
		if ready:
			data[key] = value
			object.__getattribute__(self, 'walk_data')(data)
			object.__getattribute__(self, '__write__')()
		else:
			object.__setattr__(self, key, value)
