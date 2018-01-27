##
# -*- coding: utf-8 -*-
##

class Collectable:
	'''Base class to inherit for wrapping methods into one container'''
	def __init__(self, container):
		container.append(self)
		self.container = container

	def decorate(self, func):
		self.func = func
		self.name = func.__name__
		return func

	def __call__(self, func):
		return self.decorate(func)

class event(Collectable):
	'''Wrapper for externally defined gateway events'''
	pass

class task(Collectable):
	'''Wrapper for externally defined background tasks'''
	pass
