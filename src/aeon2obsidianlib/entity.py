"""Provide a class for Aeon Timeline 2 entity representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""


class Entity:

    def __init__(self):
        self.name: str = None
        # single line text

        self.entityType: str = None
        # type ID

        self.notes: str = None
        # multiline text

    def read(self, jsonEntity: dict):
        """Read a property from Aeon 2 JSON."""
        self.name = jsonEntity['name']
        self.entityType = jsonEntity['entityType']
        self.notes = jsonEntity['notes']

