"""Component Resolvers -- These help to merge related components."""

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from pytiles import Page

class ListResolver(object):
    """List Resolver"""

    def resolve(self, list, definition_context):
        """Resolves list into definition context by retriving an existing
        list by name in the definition context attributes. If found the two
        lists will be merged if the existing allows inheritance. Otherwise,
        the list will be added if an existing list is not found.
        """
        last = definition_context.attributes.get(list.name)

        if last is not None and last.can_inherit():
            last.add(list)

            # Inherit inheritance rules.
            last.inherit = list.inherit

            definition_context.add_attribute(last)

        elif last is None:
            definition_context.add_attribute(list)


class DefinitionResolver(object):
    """Definition Resolver"""

    def __init__(self):
        self.pages = OrderedDict()

    def resolve(self, definition, definition_context):
        """Resolves definition into definition_context. Attributes
        are processed in the following order: Definition to resolve, it's
        parents, etc. There is a special case for TileType.Page attributes,
        these are queued and appended to the resolved definitions (This is
        done to ensure the pages equally recieve all available attributes).
        """

        is_root = definition.name == definition_context.name

        for name, attribute in definition.attributes.items():
            if isinstance(attribute, Page):
                # Give Page definition_context's attributes.
                attribute.attributes = definition_context.attributes

                # The dictionary key is the object id because there can be
                # other pages pulled in that have the same name.
                # (For resolving lets hope it uses the attribute.name
                # instead of the dict key)
                name = name if is_root else str(id(attribute))

                # Temporarily store Pages in an ordered dictionary then merge
                # them later, that way we won't have to deal with the issue
                # of processed pages occuring before all other attributes.
                self.pages[name] = attribute
            else:
                attribute.resolve(definition_context)
        
        # Add view-preparers.
        definition_context.preparers += definition.preparers 

        # Inherit role.
        if definition.role is not None and definition_context.role is None:
            definition_context.role = definition.role

        # Inherit template.
        if definition.template is not None and definition_context.template is None:
            definition_context.override_template(definition.template)

        if definition.is_extended():
            self.resolve(definition.extends, definition_context)

        if is_root:
            # Update attributes with Pages.
            definition_context.attributes.update(self.pages)

            # Clear temporary Page storage.
            self.pages = OrderedDict()
