#!/usr/bin/python

class ViewType(object):
	"""Supports processing files by passing them and supplied attributes
	to a special template processor or a custom implementation (format
	keywords from a dictionary, etc.)
	"""
	def __init__(self):
		self.attributes = {}
	
	def process(self, resource, attributes):
		raise NotImplementedError('Should have implemented a view processor')
