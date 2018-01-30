##
# -*- coding: utf-8 -*-
# exceptions.py
##

class MalformedError(Exception):
	pass

class LibraryError(Exception):
	pass

class CriticalError(Exception):
	pass

class NullDestinationError(Exception):
	pass

class UnknownCommandError(Exception):
	pass
