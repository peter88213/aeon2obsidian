"""Provide a class for Aeon Timeline 2 event representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from datetime import datetime
from datetime import timedelta


class Event:
    DATE_LIMIT = (datetime(1, 1, 1) - datetime.min).total_seconds()
    # Dates before 1-01-01 can not be displayed properly in novelibre

    def __init__(self):
        self.title: str = None
        # single line text

        self.relationships: dict[str, str] = None
        # key: role ID, value: entity ID

        self.values: dict[str, str] = None
        # key: property ID, value: text

        self.tags: list[str] = None

        self.date: str = None
        # ISO date string

        self.time: str = None
        # ISO time string

        self.lastsDays: int = None
        self.lastsHours: int = None
        self.lastsMinutes: int = None

    def read(self, jsonEvent: dict, tplDateGuid: str):
        """Read an event from Aeon 2 JSON."""
        self.read_title(jsonEvent)
        self.read_date(jsonEvent, tplDateGuid)
        self.read_relationships(jsonEvent)
        self.read_values(jsonEvent)
        self.read_tags(jsonEvent)

    def read_date(self, jsonEvent: dict, tplDateGuid: str):
        """Set date/time/duration from Aeon 2 JSON event dictionary."""
        timestamp = 0
        for evtRgv in jsonEvent['rangeValues']:
            if evtRgv['rangeProperty'] == tplDateGuid:
                timestamp = evtRgv['position']['timestamp']
                if timestamp >= self.DATE_LIMIT:
                    # Restrict date/time calculation to dates within novelibre's range
                    eventStart = datetime.min + timedelta(seconds=timestamp)
                    startDateTime = eventStart.isoformat().split('T')
                    self.date, self.time = startDateTime

                    # Calculate duration
                    if 'years' in evtRgv['span'] or 'months' in evtRgv['span']:
                        endYear = eventStart.year
                        endMonth = eventStart.month
                        if 'years' in evtRgv['span']:
                            endYear += evtRgv['span']['years']
                        if 'months' in evtRgv['span']:
                            endMonth += evtRgv['span']['months']
                            while endMonth > 12:
                                endMonth -= 12
                                endYear += 1
                        eventEnd = datetime(endYear, endMonth, eventStart.day)
                        eventDuration = eventEnd - datetime(eventStart.year, eventStart.month, eventStart.day)
                        lastsDays = eventDuration.days
                        lastsHours = eventDuration.seconds // 3600
                        lastsMinutes = (eventDuration.seconds % 3600) // 60
                    else:
                        lastsDays = 0
                        lastsHours = 0
                        lastsMinutes = 0
                    if 'weeks' in evtRgv['span']:
                        lastsDays += evtRgv['span']['weeks'] * 7
                    if 'days' in evtRgv['span']:
                        lastsDays += evtRgv['span']['days']
                    if 'hours' in evtRgv['span']:
                        lastsDays += evtRgv['span']['hours'] // 24
                        lastsHours += evtRgv['span']['hours'] % 24
                    if 'minutes' in evtRgv['span']:
                        lastsHours += evtRgv['span']['minutes'] // 60
                        lastsMinutes += evtRgv['span']['minutes'] % 60
                    if 'seconds' in evtRgv['span']:
                        lastsMinutes += evtRgv['span']['seconds'] // 60
                    lastsHours += lastsMinutes // 60
                    lastsMinutes %= 60
                    lastsDays += lastsHours // 24
                    lastsHours %= 24
                    self.lastsDays = lastsDays
                    self.lastsHours = lastsHours
                    self.lastsMinutes = lastsMinutes
                break

    def read_relationships(self, jsonEvent: dict):
        """Set relationships from Aeon 2 JSON event list."""
        self.relationships = {}
        for relationship in jsonEvent['relationships']:
            role = relationship.get('role', None)
            if role:
                entity = relationship.get('entity', None)
                if entity:
                    self.relationships[role] = entity

    def read_tags(self, jsonEvent: dict):
        """Set tags from Aeon 2 JSON event list."""
        self.tags = []
        for tag in jsonEvent['tags']:
            self.tags.append(tag.strip())

    def read_title(self, jsonEvent: dict):
        """Set title from Aeon 2 JSON event."""
        self.title = jsonEvent['title'].strip()

    def read_values(self, jsonEvent: dict):
        """Set values from Aeon 2 JSON event list."""
        self.values = {}
        for eventValue in jsonEvent['values']:
            eventProperty = eventValue.get('property', None)
            if eventProperty:
                val = eventValue.get('value', None)
                if val:
                    self.values[eventProperty] = val.strip()

