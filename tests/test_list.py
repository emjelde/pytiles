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

"""Test List component."""

import unittest
from pytiles import Definition, List
from pytiles.resolvers import ListResolver

class TestTileTypeList(unittest.TestCase):
    """Test Tile Type List."""

    def test_list_add(self):
        """Test adding to a List by adding another List, and a string value."""

        expected = ['Hack','the','planet']

        list = List('testList')
        list2 = List('testList2', ['the'])

        list.add('Hack')
        list.add(list2)
        list.add('planet')

        result = list.items

        print("Expected: {0}".format(expected))
        print("     Got: {0}".format(result))

        self.assertTrue(result == expected)
    

    def list_inherit_false(self, resolver):
        """See self.test_list_inherit_false"""

        expected = ['Hack']
        expected_final_inheritance = False

        definition = Definition('testDefinition')

        list = List('testList', items=['Hack'], inherit=False)
        list2 = List('testList', items=['the','planet'], resolver=resolver)

        definition.add_attribute(list)

        list2.resolve(definition)

        # Assert Items
        result = definition.attributes['testList'].items

        print("Using Resolver: {0}".format(resolver.__class__))
        print("Expected: {0}".format(expected))
        print("     Got: {0}".format(result))

        self.assertTrue(result == expected)

        # Assert Final Inheritance
        result_final_inheritance = definition.attributes['testList'].inherit

        print("Expected Final Inheritance: {0}".format(expected_final_inheritance))
        print("                       Got: {0}".format(result_final_inheritance))

        self.assertTrue(result_final_inheritance == expected_final_inheritance)
    
    def test_list_inherit_false(self):
        """Test List inheritance, this method tests a List that does not allow inheritance."""
        self.list_inherit_false(ListResolver())

    
    def list_inherit_true(self, resolver):
        """See self.test_list_inherit_true"""

        expected = ['Hack', 'the', 'planet']
        expected_final_inheritance = False

        definition = Definition('testDefinition')

        list = List('testList', items=['Hack'], inherit=True)
        list2 = List('testList', items=['the','planet'], inherit=False, resolver=resolver)

        definition.add_attribute(list)

        list2.resolve(definition)

        # Assert Items
        result = definition.attributes['testList'].items

        print("Using Resolver: {0}".format(resolver.__class__))
        print("Expected: {0}".format(expected))
        print("     Got: {0}".format(result))

        self.assertTrue(result == expected)

        # Assert Final Inheritance
        result_final_inheritance = definition.attributes['testList'].inherit

        print("Expected Final Inheritance: {0}".format(expected_final_inheritance))
        print("                       Got: {0}".format(result_final_inheritance))

        self.assertTrue(result_final_inheritance == expected_final_inheritance)

    def test_list_inherit_true(self):
        """Test List inheritance, this method tests a List that can inherit."""
        self.list_inherit_true(ListResolver())
