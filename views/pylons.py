#!/usr/bin/python

# Copyright (C) 2014 - Evan Mjelde
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
