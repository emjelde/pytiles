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

class ViewType(object):
    """Supports processing files by passing them and supplied attributes
    to a special template processor or a custom implementation (format
    keywords from a dictionary, etc.)
    """
    def __init__(self):
        self.attributes = {}
    
    def process(self, resource, attributes):
        raise NotImplementedError('Should have implemented a view processor')
