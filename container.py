"""Tile container -- Container for environment settings."""

class Container(object):
	"""Container -- holds environment settings and helper functions to
	launch templating.
	"""
	def __init__(self, attributes=None):
		"""
		Keyword arguments:
		attributes -- Attributes to add to template.
		"""
		#TODO
		pass
		
	def get_template(self, name):
		"""Get Definition (Template).
		Arguments:
		name -- Definition name.
		"""
		#TODO
		pass

	def get_definition(self):
		"""Alias to get_template"""
		self.get_template()
