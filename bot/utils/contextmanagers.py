##
# -*- coding: utf-8 -*-
##
from contextlib import contextmanager
##

@contextmanager
def ignored(*exceptions):
	try:
		yield
	except exceptions:
		pass

@contextmanager
def internal(bot):
	with ignored(AttributeError):
		yield bot.internal
