#!/usr/bin/python

import unittest
from pytiles.components import Definition, Page, List, String
from pytiles.resolvers import DefinitionResolver, ListResolver
from pytiles.renderers import DefinitionRenderer
from pytiles.views.python import PythonTemplate

class TestTileTypeComponents(unittest.TestCase):
	"""Test Tile Type components along with some of the standard
	Resolvers and Renderers
	"""

	def setUp(self):
		definition_resolver = DefinitionResolver()
		definition_renderer = DefinitionRenderer({'test':'works'})

		# Definition A Parent
		self.definition_a_parent = Definition('def_a_parent',
			resolver=definition_resolver, renderer=definition_renderer)

		# Definition A, extends definition_a_parent
		self.definition_a = Definition('def_a', extends=self.definition_a_parent,
			resolver=definition_resolver, renderer=definition_renderer)

		# List A
		self.list_a = List('list_a', items={'ruby':'dog','spot':'cat'},
			resolver=ListResolver())

		# List A (2)
		self.list_a2 = List('list_a', items={'george':'monkey','billy':'cat'},
			resolver=ListResolver())

		# String
		self.str_a = String('shout', 'Hack the planet!')

		page_layout = "<html><body>${body}</body></html>"

		# Page (Template)
		self.page_layout = Page('layout', page_layout, PythonTemplate())

		page_body = "<h2>${shout}</h2><br/>This test ${test} ;-)"

		# Page (Body)
		self.page_body = Page('body', page_body, PythonTemplate())
	
	def test_definition_renderer(self):
		"""Test Definition Resolve/Render."""
		expected = "<html><body><h2>Hack the planet!</h2><br/>This test works ;-)</body></html>"
		self.definition_a.add_attribute(self.str_a)
		self.definition_a.add_attribute(self.page_body)
		self.definition_a.template = self.page_layout
		self.definition_a.resolve()
		result = self.definition_a.render()
		print("Expected: {0}".format(expected))
		print("     Got: {0}".format(result))
		self.assertTrue(result == expected)

if __name__ == '__main__':
	unittest.main()
