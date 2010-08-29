"""Tile container -- Container for environment settings."""

class Container(object):
	"""Container -- holds environment settings and helper functions to
	launch templating.
	"""
	def __init__(self, definition_loader, view_loader=None):
		"""Create container.

		Keyword arguments:
		definition_loader -- Definition source loader.
		view_loader -- View-Type properties loader.
		"""
		self.view_loader = view_loader
		self.definition_loader = definition_loader
		
	def get_template(self, name):
		"""Get Definition (Template).

		Arguments:
		name -- Definition name.
		"""
		# TODO: Add Definition reader here
		#
		# definition_reader.register_pattern_resolver('REGEX', new RegExPatternEvaluator())
		# definition_reader.register_pattern_resolver('WILDCARD', new WildcardPatternEvaluator())
		#
		# return definition_reader.get_definition(name)
		pass

	def get_definition(self):
		"""Alias to get_template"""
		self.get_template()
