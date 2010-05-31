#!/usr/bin/python

from string import Template 
from pytiles.views.viewtype import ViewType

class PythonTemplate(ViewType):
	"""View Type using Python string Template class."""

	def process(self, resource, attributes):
		"""Process view type by creating a Template from the resource
		string and substituting attributes.
		"""
		template = Template(resource)
		return template.substitute(attributes)
