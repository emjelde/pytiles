#!/usr/bin/python

from string import Template 
from pytiles.views.viewtype import ViewType
from pytiles.errors import TilesError

class PythonTemplate(ViewType):
	"""View Type using Python string Template class."""

	def process(self, resource, attributes):
		"""Process view type by creating a Template from the resource
		string and substituting attributes.
		"""
		template = Template(resource)

		try:
			return template.substitute(attributes)
		except KeyError as err:
			raise TilesError("Template is missing {0} key".format(err))

class PythonString(ViewType):
	"""View Type using Python string format."""

	def process(self, resource, attributes):
		"""Process view type by replacing value holders ex: %(name) 
		from the resource string
		"""
		try:
			return resource % attributes
		except KeyError as err:
			raise TilesError("Template is missing {0} key".format(err))
