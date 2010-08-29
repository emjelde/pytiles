"""Test component resolution."""

import unittest
from pytiles import Definition, Page, List, String
from pytiles.resolvers import DefinitionResolver, ListResolver
from pytiles.renderers import DefinitionRenderer
from pytiles.views.python import PythonTemplate
from pytiles import TilesError

class TestTileTypeResolveRender(unittest.TestCase):
	"""Test standard TileType Resolvers and Renderers."""	

	def test_resolve_renderer_simple(self):
		"""Test Definition Resolve/Render (Simple)."""

		expected = "<html><body><h2>Hack the planet!</h2><br/>This test works ;-)</body></html>"

		definition_resolver = DefinitionResolver()
		definition_renderer = DefinitionRenderer({'test':'works'})

		# Definition A Parent
		definition_a_parent = Definition('def_a_parent',
			resolver=definition_resolver, renderer=definition_renderer)

		# Definition A, extends definition_a_parent
		definition_a = Definition('def_a', extends=definition_a_parent,
			resolver=definition_resolver, renderer=definition_renderer)

		# List A
		list_a = List('list_a', items={'ruby':'dog','spot':'cat'},
			resolver=ListResolver())

		# List A (2)
		list_a2 = List('list_a', items={'george':'monkey','billy':'cat'},
			resolver=ListResolver())

		# String
		str_a = String('shout', 'Hack the planet!')

		page_layout = "<html><body>${body}</body></html>"

		# Page (Template)
		page_layout = Page('layout', page_layout, PythonTemplate())

		page_body = "<h2>${shout}</h2><br/>This test ${test} ;-)"

		# Page (Body)
		page_body = Page('body', page_body, PythonTemplate())

		definition_a.add_attribute(str_a)
		definition_a.add_attribute(page_body)
		definition_a.template = page_layout
		definition_a.resolve()
		result = definition_a.render()
		print("Expected: {0}".format(expected))
		print("     Got: {0}".format(result))
		self.assertTrue(result == expected)


	def test_resolve_renderer_multiple_levels_of_inheritance(self):
		"""Test Definition Resolve/Render (Multiple Levels of Inheritance)."""

		expected = "<html><body>Can I get a Woot Woot! ;-)</body></html>"

		definition_resolver = DefinitionResolver()
		definition_renderer = DefinitionRenderer()

		# Definition Root 
		definition_root = Definition('def_root',
			resolver=definition_resolver, renderer=definition_renderer)

		definition_root.template = Page('layout',
			"<html><body>${body}</body></html>", PythonTemplate())

		# Definition A 
		definition_a = Definition('def_a', extends=definition_root,
			resolver=definition_resolver, renderer=definition_renderer)

		definition_a.add_attribute('Woot Woot!', key='say_what')

		# Definition B
		definition_b = Definition('def_b', extends=definition_a,
			resolver=definition_resolver, renderer=definition_renderer)

		definition_b.add_attribute(Page('body', "$body ;-)", PythonTemplate()))

		# Definition C
		definition_c = Definition('def_c', extends=definition_b,
			resolver=definition_resolver, renderer=definition_renderer)

		definition_c.add_attribute(Page('body', "Can I get a $say_what", PythonTemplate()))

		result = str(definition_c)

		print("Expected: {0}".format(expected))
		print("     Got: {0}".format(result))
		self.assertTrue(result == expected)
	
	def test_resolve_render_definition_as_template(self):
		"""Test Definition Resolve/Render (Definition with Definition as a Template)."""

		expected = "<html><body>Hello World</body></html>"

		definition_resolver = DefinitionResolver()
		definition_renderer = DefinitionRenderer()

		# Template Definition
		definition_template = Definition('def_template',
			resolver=definition_resolver, renderer=definition_renderer,
			template=Page('layout', "<html><body>$greeting $who</body></html>", PythonTemplate()))

		definition_template.add_attribute('Hello', key='greeting')

		definition = Definition('def', resolver=definition_resolver,
			renderer=definition_renderer, template=definition_template)

		definition.add_attribute('World', key='who')

		result = str(definition)

		print("Expected: {0}".format(expected))
		print("     Got: {0}".format(result))
		self.assertTrue(result == expected)
