"""Component Renderers -- These help to render components."""

from pytiles import TilesError

class DefinitionRenderer:
	"""Definition Renderer"""

	def __init__(self, attributes=None):
		"""Initialize DefinitionRenderer

		Keyword arguments:
		attributes -- Attributes to add to the template.
		"""
		self.external_attributes = attributes if \
			attributes is not None else {}

	def render(self, definition):
		"""Render definition

		Keyword arguments:
		attributes -- Extra attributes to add to the template.
		"""
		# Merge external attributes.
		for key, value in self.external_attributes.items():
			# Adding here will also add it again later when
			# processing attributes, how to fix?
			definition.add_attribute(value, key=key)

		# Invoke any View Preparers.
		for preparer in definition.preparers:
			preparer.execute(definition, definition.attributes)

		# Process attributes
		for attribute in definition.attributes.values():
			rendition = attribute.render()
			if rendition != '':
				definition.add_attribute(rendition, key=attribute.name)

		# Finally, add our attributes to the template.
		try:
			definition.template.add_attributes(definition.attributes)
		except AttributeError:
			# Try Definition given as a template.
			for attribute in definition.attributes.values():
				definition.template.add_attribute(attribute)

		# Party time!
		try:
			return definition.template.render()
		except AttributeError:
			if definition.template is None:
				raise TilesError("Template was never set in {0} definition" \
					.format(definition.name), code=TilesError.NO_TEMPLATE)
			else:
				raise
