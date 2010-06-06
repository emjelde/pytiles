#!/usr/bin/python

"""Tile components -- These are the fundamental components used form a layout."""

try:
	from collections import OrderedDict
except ImportError:
	from ordereddict import OrderedDict

from pytiles.errors import TilesError

class TileType(object):
	"""A page component that can be evaluated to a string when ready to be displayed."""

	def __init__(self, name, resolver=None, renderer=None, role=None, in_role=lambda role: True):
		"""Keyword arguments:
		   resolver -- Function that will resolve Tile Type into the current execution state.
		   renderer -- Function that will render Tile Type to a string.
		   role     -- Role which can be evaluated for rendering display permission.
		   in_role  -- Function to use to evaluate roles which must return a bool type,
		               If no function supplied default will always return True.
		"""
		self.name = name
		self.resolver = resolver
		self.renderer = renderer
		self.role = role
		# Alternative way to specify in role function. 
		if 'tiles_in_role' in globals():
			self.in_role = globals()['tiles_in_role']
		else:
			self.in_role = in_role
	
	def resolve(self, definition_context):
		"""Resolve Tile Type component

		Arguments:
		definition_context -- Encapsulation of the current state of execution.
		"""
		if self.resolver is None:
			definition_context.add_attribute(self)
		else:
			try:
				self.resolver.resolve(self, definition_context)
			except AttributeError:
				raise NotImplementedError("Should have implemented a resolver for {0}".format(self.name))

	def render(self):
		"""Render Tile Type component."""
		try:
			if self.can_render():
				return self.renderer.render(self)
		except AttributeError:
			raise NotImplementedError("Should have implemented a renderer for {0}".format(self.name))
		return ''

	def can_render(self):
		"""Returns a boolean value for permission given to render the component."""
		in_role = self.in_role(self.role)
		if type(in_role) is not bool:
			raise TilesError("Function '{0}' must return a boolean value.".format(self.in_role.__name__))
		return in_role

	def __repr__(self):
		return "{0}({1!r})".format(self.__class__, self.__dict__);

	def __str__(self):
		return self.render()


class String(TileType):
	"""A very simple single value page component."""

	def __init__(self, name, value, **kwargs):
		self.value = value
		super(String, self).__init__(name, **kwargs)
	
	def render(self):
		if self.can_render():
			return self.value
		return ''


class List(TileType):
	"""A collection of other Tile Types."""

	def __init__(self, name, items=None, inherit=True, **kwargs):
		"""Keyword arguments:
		   items   -- Array of initial items.
		   inherit -- Lets you know if it should inherit items on merge. (Default: True)
		"""
		self.items = items if items is not None else []
		self.inherit = inherit
		super(List, self).__init__(name, **kwargs)
	
	def add(self, item, order = 'append'):
		"""Add Item to list.

		Keyword arguments:
		item  -- If item is instance of TileType.List the list items will be
		         merged, otherwise items will be processed as normal.
		order -- order values can be 'append' or 'prepend', which will do excatly
		         what you would expect (Default: append).
		"""
		try:
			item = item.items
		except AttributeError:
			item = [item]

		self.items = {
			'prepend': item + self.items,
			 'append': self.items + item
		}[order]
	
	def can_inherit(self):
		return self.inherit
	
	def render(self):
		"""Generate unordered list of items. (For LOLs)."""
		if self.can_render():
			output = '<ul>'
			for item in self.items:
				output += "<li>{0}</li>".format(item)
			return output + '</ul>'
		return ''


class Page(TileType):
	"""Page component support in rendering of pages, it is responsible for
	holding Attributes (rendered Tile Types)
	which can later be used to fill the page.
	"""

	def __init__(self, name, resource, view_type, **kwargs):
		"""Keyword arguments:
		   resource -- Page resource (file path, stream, string, etc) 
		   viewtype -- View Type class instance
		"""
		self.resource = resource
		self.view_type = view_type
		self.attributes = {}
		super(Page, self).__init__(name, **kwargs)
	
	def add_attributes(self, attributes):
		"""Add attributes merges with present attributes."""
		self.attributes = dict(self.attributes, **attributes)
	
	def render(self):
		if self.can_render():
			return self.view_type.process(self.resource, self.attributes)
		return ''


class Definition(TileType):
	"""Encapsulates other Tile Types in for a complete template composition.
	It can function as an abstract definition where no template is defined,
	in which it will extend/or inherit other definitions.
	"""

	def __init__(self, name, extends=None, template=None, **kwargs):
		"""Keyword arguments:
		   extends   -- Definition Tile Type parent of this class
		   template  -- Page Tile Type
		   resolver  -- Resolver (see pytiles.resolvers.DefinitionResolver)
		   renderer  -- Renderer (see pytiles.renderers.DefinitionRenderer)
		"""
		self._parent = extends
		self.template = template
		self.attributes = OrderedDict()
		self.preparers = []
		self.__resolved = False
		super(Definition, self).__init__(name, **kwargs)
		
	@property
	def extends(self):
		"""Parent definition."""
		return self._parent
	
	@extends.setter
	def extends(self, parent):
		"""Set definition to extend."""
		self._parent = parent
		self.__resolved = False

	def add_preparer(self, view_preparer):
		"""Add to View Preparers."""
		self.preparers.append(classpath)
	
	def add_attribute(self, attribute, key=None):
		"""Add attributes, attribute can be an instance of TileType,
		or some other value as long as a key is given.

		Keyword arguments:
		key -- String key to store the attribute into.
		"""
		if isinstance(attribute, TileType):
			key = attribute.name if key is None else key
			self.attributes[key] = attribute
		else:
			key = key if key is not None else str(id(attribute))
			self.attributes[key] = String(key, attribute)

	def override_template(self, template, merge=True):
		"""Keyword arguments:
		   template -- Page Tile Type 
		   merge    -- If True attributes of given template will be merged
		               with the overridden template
		"""
		if merge and self.template is not None:
			template.addattributes(self.template.attributes)

		self.template = template
	
	def is_extended(self):
		"""Check if definition has any parents, therefore has been extended."""
		return self._parent is not None
	
	def resolve(self, definition_context=None):
		"""Passes the Definition to a resolver, the expected result should be a
		definition that has been merged with it's parents."""

		definition_context = self if definition_context is None else definition_context

		super(Definition, self).resolve(definition_context)

		# All parent definitions should now be "merged" into
		# this definition, parent no longer needed.
		self._parent = None

		self.__resolved = True
	
	def render(self):
		"""Render Definition, if the definition has not been resolved, the
		resolver will be called before rendering.
		"""
		if not self.__resolved:
			self.resolve(self)

		return super(Definition, self).render()
