#!/usr/bin/python

"""Component Resolvers -- These help to merge related components."""

try:
	from collections import OrderedDict
except ImportError:
	from ordereddict import OrderedDict

from pytiles.components import Page

class ListResolver(object):
	"""List Resolver"""

	def resolve(self, list, definition_context):
		"""Resolves list into definition context by retriving an existing
		list by name in the definition context attributes. If found the two
		lists will be merged if the existing allows inheritance. Otherwise,
		the list will be added if an existing list is not found.
		"""
		last = definition_context.attributes.get(list.name)

		if last is not None and last.can_inherit():
			last.add(list)

			# Inherit inheritance rules.
			last.inherit = list.inherit

			definition_context.add_attribute(last)

		elif last is None:
			definition_context.add_attribute(list)

class DefinitionResolver(object):
	"""Definition Resolver"""

	def __init__(self):
		self.pages = OrderedDict()

	def resolve(self, definition, definition_context):
		"""Resolves definition into definition_context."""
		for name, attribute in definition.attributes.items():
			if isinstance(attribute, Page):
				# Give Page definition_context's attributes
				attribute.attributes = definition_context.attributes

				# Temporarily store Pages in an ordered dictionary then merge
				# them later, that way we won't have to deal with the issue
				# of processed pages occuring before all other attributes.
				self.pages[attribute.name] = attribute
			else:
				attribute.resolve(definition_context)
		
		for preparers in definition.preparers:
			definition_context.add_preparer(preparers)

		if definition.role is not None and definition_context.role is None:
			definition_context.role = definition.role

		if definition.template is not None and definition_context.template is None:
			definition_context.override_template(definition.template)

		if definition.is_extended():
			self.resolve(definition.extends, definition_context)

		if definition.name == definition_context.name:
			# Update attributes with Pages.
			definition_context.attributes.update(self.pages)

		# Clear temporary Page storage.
		self.pages = OrderedDict()
