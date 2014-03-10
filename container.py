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

"""Tile container -- Container for environment settings."""

class Container(object):
    """Container -- holds environment settings and helper functions to
    launch templating.
    """
    def __init__(self, definition_loader, view_loader=None):
        """Create container.

        Keyword arguments:
        definition_loader -- Definition source loader.
        view_loader -- View-Type properties loader.
        """
        self.view_loader = view_loader
        self.definition_loader = definition_loader
        
    def get_template(self, name):
        """Get Definition (Template).

        Arguments:
        name -- Definition name.
        """
        # TODO: Add Definition reader here
        #
        # definition_reader.register_pattern_resolver('REGEX', new RegExPatternEvaluator())
        # definition_reader.register_pattern_resolver('WILDCARD', new WildcardPatternEvaluator())
        #
        # return definition_reader.get_definition(name)
        pass

    def get_definition(self):
        """Alias to get_template"""
        self.get_template()
