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

"""Python view types."""

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
