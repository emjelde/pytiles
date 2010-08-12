#!/usr/bin/python

import os
import unittest
from pytiles.components import Page
from pytiles.views.python import PythonTemplate, PythonString

class TestTileTypePage(unittest.TestCase):
	"""Test Tile Type Page."""

	def test_page_add_attributes(self):
		"""Test adding attributes to a Page."""

		expected = {'eat':"spam & eggs", 'drink':"good ol' h2O"}

		page = Page('testPage', None, None)
		page.add_attributes({'eat':"spam & eggs"})
		page.add_attributes({'drink':"good ol' h2O"})

		result = page.attributes

		print("Expected: {0}".format(expected))
		print("     Got: {0}".format(result))

		self.assertTrue(result == expected)


	def page_render(self, expected, resource, view_type):
		"""See self.test_page_render"""
		
		page = Page('testPage', resource, view_type)
		page.add_attributes({'title': "Welcome", 'name': 'pyTiles'})

		result = page.render()

		print("Using View Type: {0}".format(view_type.__class__))
		print("Expected: {0}".format(expected))
		print("     Got: {0}".format(result))

		self.assertTrue(result == expected)
	
	def test_page_render(self):
		"""Test page render with View Types."""
		dir = os.path.dirname(__file__)

		# Test Python Template
		python_template_expected = os.path.join(dir, 'resources/page_render_pythontemplate_expected.html')
		python_template = os.path.join(dir, 'resources/page_render_pythontemplate.html')
		self.page_render(
			open(python_template_expected).read(),
			open(python_template).read(),
			PythonTemplate())

		# Test Python String
		python_string_expected = os.path.join(dir, 'resources/page_render_pythonstring_expected.html')
		python_string = os.path.join(dir, 'resources/page_render_pythonstring.html')
		self.page_render(
			open(python_string_expected).read(),
			open(python_string).read(),
			PythonString())
