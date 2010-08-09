#!/usr/bin/python

class TilesError(Exception):
	"""Tiles Error

	Class constants:
	FILE_NOT_FOUND     -- For files not found.
	NO_TEMPLATE        -- 
	NO_SUCH_PREPARER   --
	NO_SUCH_DEFINITION --
	"""
	FILE_NOT_FOUND = 404
	EMPTY_TEMPLATE = 1

	def __init__(self, value, code=None):
		"""Keyword arguments:
		code -- See TilesException class constants."""
		self.value = value
		self.code = code

	def __str__(self):
		return repr(self.value)
