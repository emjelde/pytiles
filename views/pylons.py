"""Pylons render function."""

from webhelpers.html import literal

import pylons
from pylons.templating import pylons_globals, cached_template

def render_pytiles(template_name, extra_vars=None, cache_key=None,
					cache_type=None, cache_expire=None):
	"""Render a template with Pytiles"""
	# Create a render callable for the cache function
	def render_template():
		# Pull in extra vars if needed
		globs = extra_vars or {}

		# Second, get the globals
		globs.update(pylons_globals())

		# Grab a template reference
		template = \
			globs['app_globals'].pytiles_container.get_template(template_name)

		return literal(template.render(**globs))
	
	return cached_template(template_name, render_template, cache_key=cache_key,
							cache_type=cache_type, cache_expire=cache_expire)
