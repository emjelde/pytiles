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

"""PyTiles custom errors."""

class TilesError(Exception):
    """Tiles Error

    Class constants:
    FILE_NOT_FOUND     -- For files not found.
    NO_TEMPLATE        -- 
    NO_SUCH_PREPARER   --
    NO_SUCH_DEFINITION --
    """
    FILE_NOT_FOUND = 404
    EMPTY_TEMPLATE = 1

    def __init__(self, value, code=None):
        """Keyword arguments:
        code -- See TilesException class constants."""
        self.value = value
        self.code = code

    def __str__(self):
        return repr(self.value)
