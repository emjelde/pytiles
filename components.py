#!/usr/bin/python

"""Tile components -- These are the fundamental components used form a layout."""

class TileType(object):
	"""A page component that can be evaluated to a string when ready to be displayed."""
	def __init__(self, name, role=None, in_role=lambda role: True):
		"""Keyword arguments:
		   role    -- Role which can be evaluated for rendering display permission.
		   in_role -- Function to use to evaluate roles which must return a bool type,
		              If no function supplied default will always return True.
		"""
		self.name = name
		self.role = role
		# Alternative way to specify in role function. 
		if 'tiles_in_role' in globals():
			self.in_role = globals()['tiles_in_role']
		else:
			self.in_role = in_role

	def render(self):
		"""Render Tile Type component, children must implement this method in their own way."""
		raise NotImplementedError("Should have implemented this")

	def can_render(self):
		"""Returns a boolean value for permission given to render the component."""
		in_role = self.in_role(self.role)
		if type(in_role) is not bool:
			raise Exception("Function '{0}' must return a boolean value.".format(self.in_role.__name__))
		return in_role

	def __repr__(self):
		return "{0}({1!r})".format(self.__class__, self.__dict__);

	def __str__(self):
		return self.render()

class String(TileType):
	"""A very simple single value page component."""
	def __init__(self, name, value, role=None):
		self.value = value
		super(String, self).__init__(name, role)
	
	def render(self):
		if self.can_render():
			return self.value
		return ''

class List(TileType):
	"""A collection of other Tile Types."""
	def __init__(self, name, items=None, inherit=True, role=None):
		"""Keyword arguments:
		   items   -- Array of initial items.
		   inherit -- Lets you know if it should inherit items on merge. (Default: True)
		"""
		self.items = items if items is not None else []
		self.inherit = inherit
		super(List, self).__init__(name, role)
	
	def add(self, item, order = 'append'):
		"""Add Item to list.

		Keyword arguments:
		item  -- If item is instance of TileType.List the list items will be
		         merged, otherwise items will be processed as normal.
		order -- order values can be 'append' or 'prepend', which will do excatly
		         what you would expect (Default: append).
		"""
		if isinstance(item, List):
			item = item.items

		self.items = {
			'prepend': item + self.items,
			 'append': self.items + item
		}[order]
	
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
	which can later be used to fill the page."""
	def __init__(self, name, page, view_type, role=None):
		"""Keyword arguments:
		   page     -- File path to page
		   viewtype -- View Type class instance
		"""
		self.page = page
		self.view_type = view_type
		self.attributes = {}
		super(Page, self).__init__(name, role)
	
	def add_attributes(attributes):
		"""Add attributes merges with present attributes."""
		self.attributes = dict(self.attributes, **attributes)
	
	def render(self):
		if self.can_render():
			return self.view_type.process(self.page, self.attributes)
		return ''

class Definition(TileType):
	"""Encapsulates other Tile Types in for a complete template composition.
	It can function as an abstract definition where no template is defined,
	in which it will extend/or inherit other definitions."""
	def __init__(self, name, processor_builder, extends=None, template=None, role=None):
		"""Keyword arguments:
		   processor_builder -- Definition Processor Builder implementation
		   extends           -- Definition Tile Type parent of this class
		   template          -- Page Tile Type
		"""
		self.processor_builder = processor_builder
		self._parent = extends
		self.template = template
		self.attributes = {}
		self._preparers = []
		self.__resolved = False
		super(Definition, self).__init__(name, role)
	
	@property
	def preparers(self):
		"""View Preparers."""
		return self._preparers

	def add_preparer(self, classpath):
		"""Add to View Preparers."""
		if classpath not in self._preparers:
			self._preparers.append(classpath)
	
	@property
	def extends(self):
		"""Parent definition."""
		return self._parent
	
	@extends.setter
	def extends(self, parent):
		"""Set definition to extend."""
		self._parent = parent
		self.__resolved = False

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
	
	def resolve(self):
		"""Passes the Definition to a processor provided by the Processor Builder,
		the expected result should be a definition that has been merged with it's
		parents."""
		self.processor_builder.processor.resolve(self)

		# All parent definitions should now be "merged" into
		# this definition, parent no longer needed.
		self._parent = None

		self.__resolved = True
	
	def render(self):
		if self.can_render():
			return self.processor_builder.processor.process(self)
		return ''

def main():
	pass

if __name__ == '__main__':
	main()
