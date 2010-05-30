#!/usr/bin/python

"""Component Renderers -- These help to render components."""

import pytiles.errors

class DefinitionRenderer:
	"""Definition Renderer"""
	def __init__(self, attributes=None):
		self.external_attributes = attributes if \
			attributes is not None else []

	def render(self, definition):
		"""Render definition"""
		# Process attributes
		for attribute in definition.attributes:
			rendition = attribute.render()
			if rendition != '':
				definition.add_attribute(rendition, key=attribute.name)

		# Merge external attributes.
		if self.external_attributes is not None:
			for key, value in self.external_attributes:
				definition.add_attribute(value,key=key)

		# Invoke any View Preparers.
		for preparer in definition.preparers:
			preparer.execute(definition, definition.attributes)

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
				.format(definition.name), code=TilesError.EMPTY_TEMPLATE)
