"""Provide a class for the Aeon Timeline 2 data model.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from aeon2obsidianlib.event import Event
from aeon2obsidianlib.entity import Entity


class Timeline:

    def __init__(self):

        # Strategies:
        self.entityClass = Entity
        self.eventClass = Event

        self.types: dict[str, str] = {}
        # key: ID, value: name

        self.roles: dict[str, str] = {}
        # key: ID, value: name

        self.properties: dict[str, str] = {}
        # key: ID, value: name

        self.entities: dict[str, Entity] = {}
        # key: ID, value: entityClass instance

        self.events: dict[str, Event] = {}
        # key: ID, value: eventClass instance

        self.entitiesByType: dict[str, list[str]] = {}
        # key: type ID, value: list of entity IDs
