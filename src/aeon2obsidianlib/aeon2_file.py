"""Provide a class for Aeon Timeline 2 'aeon' file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon3yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import json
from aeon2obsidianlib.aeon2_fop import open_timeline
from datetime import datetime
from datetime import timedelta
from datetime import date


class Aeon2File:

    def __init__(self, filePath):
        """Set the Aeon 2 project file path."""
        self.filePath = filePath
        self.types = {}
        self.roles = {}
        self.entities = {}

        self.items = {}
        self.labels = {}
        self.itemIndex = {}
        self.relationships = {}
        self.tags = {}
        self.narrative = {}

    def read(self):
        """Read the Aeon 2 project file.
        
        Store the relevant data in the items dictionary.
        Populate the labels dictionary.
        Populate the itemIndex dictionary.
        
        Return a success message.
        """

        def add_label(key, value):
            """Add an entry to the labels dictionary, handling multiple labels."""
            if value in labelText:
                print(f'Multiple label: {value}')
                number = labelText[value] + 1
                labelText[value] = number
                value = f'{value}({number})'
            else:
                labelText[value] = 0
            self.labels[key] = value

        #--- Read the aeon file and get a JSON data structure.
        jsonData = open_timeline(self.filePath)
        labelText = {}

        #--- Create a labels dictionary for types and relationships.
        for aeonType in jsonData['template']['types']:
            uid = aeonType['guid']
            item = aeonType.get('name', '').strip()
            if item:
                add_label(uid, item)
            for role in aeonType['roles']:
                add_label(role['guid'], role['name'])
            return
        for uid in jsonData['template']['references']:
            reference = jsonData['template']['references'][uid].get('name', '').strip()
            if reference:
                self.labels[uid] = reference

        #--- Create a data model and extend the labels dictionary.
        for uid in jsonData['data']['items']:
            aeonItem = jsonData['data']['items'][uid]
            add_label(uid, aeonItem['name'].strip())
            self.items[uid] = self._get_item(aeonItem)

        #--- Create an index.
        for uid in jsonData['data']['items']['allIdsForType']:
            itemUidList = jsonData['data']['items']['allIdsForType'][uid]
            self.itemIndex[uid] = itemUidList

        #--- Create a relationships dictionary.
        for uid in jsonData['data']['relationships']:
            refId = jsonData['data']['relationships'][uid]['reference']
            objId = jsonData['data']['relationships'][uid]['object']
            self.relationships[uid] = (refId, objId)

        #--- Get the narrative tree.
        self.narrative = jsonData['data'].get('narrative', self.narrative)

        return 'Aeon 2 file successfully read.'

    def _get_date(self, aeonItem):
        timestamp = aeonItem['startDate'].get('timestamp', 'null')
        if timestamp and timestamp != 'null':
            startDateTime = datetime.min + timedelta(seconds=timestamp)
            dateStr = date.isoformat(startDateTime)
        else:
            dateStr = ''
        return dateStr

    def _get_duration(self, aeonItem):
        durationList = []
        durationDict = aeonItem.get('duration', None)
        if durationDict:
            durations = list(durationDict)
            for unit in durations:
                if durationDict[unit]:
                    durationList.append(f'{durationDict[unit]} {unit}')
        durationStr = ', '.join(durationList)
        return durationStr

    def _get_item(self, aeonItem):
        """Return a dictionary with the relevant item properties."""
        item = {}
        item['shortLabel'] = aeonItem['shortLabel']
        item['summary'] = aeonItem['summary']
        item['references'] = aeonItem['references']
        item['children'] = aeonItem['children']

        # Read tags.
        tags = []
        for tag in aeonItem['tags']:
            tags.append(f"#{tag.strip().replace(' ','_')}")
            item['tags'] = tags

        # Read date/time/duration.
        dateStr = self._get_date(aeonItem)
        if dateStr:
            item['Date'] = dateStr
        timeStr = self._get_time(aeonItem)
        if timeStr:
            item['Time'] = timeStr
        durationStr = self._get_duration(aeonItem)
        if durationStr:
            item['Duration'] = durationStr

        return item

    def _get_time(self, aeonItem):
        timestamp = aeonItem['startDate'].get('timestamp', 'null')
        if timestamp and timestamp != 'null':
            startDateTime = datetime.min + timedelta(seconds=timestamp)
            timeStr = startDateTime.strftime('%X')
            seconds = aeonItem['startDate'].get('second', 0)
            if not seconds:
                h, m, _ = timeStr.split(':')
                timeStr = ':'.join([h, m])
        else:
            timeStr = ''
        return timeStr

