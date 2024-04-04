"""Provide a class for Aeon Timeline 2 'aeon' file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from aeon2obsidianlib.aeon2_fop import open_timeline
from aeon2obsidianlib.timeline import Timeline


class Aeon2File:

    def __init__(self, filePath: str):
        """Set the Aeon 2 project file path."""
        self.filePath = filePath
        self.timeline: Timeline = None

    def read(self):
        """Read the Aeon 2 project file.
        
        Return a success message.
        """

        #--- Read the aeon file and get a JSON data structure.
        jsonData = open_timeline(self.filePath)

        #--- Get the date definition.
        for tplRgp in jsonData['template']['rangeProperties']:
            if tplRgp['type'] == 'date':
                for tplRgpCalEra in tplRgp['calendar']['eras']:
                    if tplRgpCalEra['name'] == 'AD':
                        tplDateGuid = tplRgp['guid']
                        break

        #--- Read type and role names.
        for jsonType in jsonData['template']['types']:
            uid = jsonType['guid']
            name = jsonType['name']
            self.timeline.types[uid] = name
            self.timeline.entitiesByType[uid] = []
            for jsonRole in jsonType['roles']:
                uid = jsonRole['guid']
                name = jsonRole['name']
                self.timeline.roles[uid] = name

        #--- Read property names.
        for jsonProperty in jsonData['template']['properties']:
            uid = jsonProperty['guid']
            name = jsonProperty['name']
            self.timeline.properties[uid] = name

        #--- Read entities.
        for jsonEntity in jsonData['entities']:
            uid = jsonEntity['guid']
            self.timeline.entities[uid] = self.timeline.entityClass()
            self.timeline.entities[uid].read(jsonEntity)
            self.timeline.entitiesByType[jsonEntity['entityType']].append(uid)

        #--- Read events.
        for jsonEvent in jsonData['events']:
            uid = jsonEvent['guid']
            self.timeline.events[uid] = self.timeline.eventClass()
            self.timeline.events[uid].read(jsonEvent, tplDateGuid)

        return 'Aeon 2 file successfully read.'
