#!/usr/bin/python

"""Component Renderers -- These help to render components."""

from pytiles.errors import TilesError

class DefinitionRenderer:
	"""Definition Renderer"""

	def __init__(self, attributes=None):
		self.external_attributes = attributes if \
			attributes is not None else {}

	def render(self, definition):
		"""Render definition"""
		# Merge external attributes.
		if self.external_attributes is not None:
			#definition.attributes = dict(self.external_attributes,
			#	**definition.attributes)
			### OR ###
			for key, value in self.external_attributes.items():
				# Adding here will also add it again later when
				# processing attributes, how to fix?
				definition.add_attribute(value, key=key)
			### OR ###
			#try:
			#	definition.template.add_attributes(self.external_attributes)
			#except AttributeError:
			#	raise TilesError("Template was never set in {0} definition" \
			#		.format(definition.name), code=TilesError.NO_TEMPLATE)

		# Invoke any View Preparers.
		for preparer in definition.preparers:
			preparer.execute(definition, definition.attributes)

		# Process attributes
		for attribute in definition.attributes.values():
			rendition = attribute.render()
			if rendition != '':
				definition.add_attribute(rendition, key=attribute.name)

		# Finally, add our attributes to the template
		try:
			definition.template.add_attributes(definition.attributes)
		except AttributeError:
			definition.template.attributes = definition.attributes

		# Party time!
		try:
			return definition.template.render()
		except AttributeError:
			raise TilesError("Template was never set in {0} definition" \
				.format(definition.name), code=TilesError.NO_TEMPLATE)
