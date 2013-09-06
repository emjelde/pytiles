#!/usr/bin/python

import re
from lxml import etree

class DecideTileTypeExtElement(etree.XSLTExtension):
    """Decide Tile Type XSLT Extension
    Evaluates the attribute's value to determine what kind of tile
    type component the attribute likely represents.

    If the value starts with a forward slash or ends with a dot
    followed by one or more characters then the type will be TileType.Page.

    If the value matches a definition name, then the type will be TileType.Definition.

    The last resort is a type TileType.String.  
    """
    def __init__(self, definitions=[]):
        """Keyword arguments:
           definitions -- List of definition names used to match Definition types.
        """
        self.definitions = definitions

    def execute(self, context, self_node, input_node, output_parent):
        value = input_node.attrib['value']

        if re.search('^\/|\.\w{1,}$', value):
            output_parent.text = 'page'

        elif value in self.definitions:
            output_parent.text = 'definition'

        else:
            output_parent.text = 'string'

        output_parent.extend(list(self_node))
