"""Provide a base class for Markdown export from Aeon Timeline 2.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from aeon2obsidianlib.event import Event
from re._compiler import isstring


class ObsidianFiles:
    FORBIDDEN_CHARACTERS = ('\\', '/', ':', '*', '?', '"', '<', '>', '|')
    # set of characters that filenames cannot contain

    def __init__(self, folderPath:str):
        """Set the Obsidian folder."""
        self.folderPath = folderPath
        self.timeline = None

    def write(self) -> str:
        """Create a set of Markdown files in the Obsidian folder.
        
        Return a success message.
        """
        os.makedirs(self.folderPath, exist_ok=True)
        self._build_index()

        for uid in self.timeline.entities:
            entity = self.timeline.entities[uid]
            name = self._strip_title(entity.name)
            text = self._to_markdown(entity.notes)
            self._write_file(f'{self.folderPath}/{name}.md', text)

        for uid in self.timeline.events:
            event = self.timeline.events[uid]
            title = self._strip_title(event.title)
            text = self._build_content(event)
            self._write_file(f'{self.folderPath}/{title}.md', text)

        return 'Obsidian files successfully written.'

    def _build_content(self, event:Event) -> str:
        """Return a string with the Markdown file content.
        
        Positional arguments:
            event: Event instance.
        """
        lines = []
        for propertyId in event.values:
            propertyName = self.timeline.properties[propertyId]
            lines.append(f'### {propertyName}')
            eventValue = event.values[propertyId]
            if eventValue and type(eventValue) == str:
                lines.append(self._to_markdown(eventValue))

        for roleId in event.relationships:
            roleName = self.timeline.roles[roleId]
            entityId = event.relationships[roleId]
            entityName = self.timeline.entities[entityId].name
            link = self._strip_title(entityName)
            lines.append(f'- {roleName}: [[{link}]]')
        for tag in event.tags:
            lines.append(f"#{tag.replace(' ', '_')}")
        lines.append(event.date)
        lines.append(event.time)
        return '\n\n'.join(lines)

    def _build_index(self):
        """Create index pages."""
        mainIndexlines = []

        #--- Create an index file with the events.
        mainIndexlines.append(f'- [[__events]]')
        lines = []
        for uid in self.timeline.events:
            eventTitle = self.timeline.events[uid].title
            lines.append(f'- [[{self._strip_title(eventTitle)}]]')
        text = '\n'.join(lines)
        self._write_file(f'{self.folderPath}/__events.md', text)

        for typeUid in self.timeline.entitiesByType:
            entityType = f'_{self._strip_title(self.timeline.types[typeUid])}'
            mainIndexlines.append(f'- [[{entityType}]]')
            entityUidList = self.timeline.entitiesByType[typeUid]

            #--- Create an index file with the entities of the type.
            lines = []
            for entityUid in entityUidList:
                entityName = self.timeline.entities[entityUid].name
                lines.append(f'- [[{self._strip_title(entityName)}]]')
            text = '\n'.join(lines)
            self._write_file(f'{self.folderPath}/{entityType}.md', text)

        #--- Create a main index file with the types and event link.
        text = '\n'.join(mainIndexlines)
        self._write_file(f'{self.folderPath}/__index.md', text)

    def _strip_title(self, title: str) -> str:
        """Return title with characters removed that must not appear in a file name."""
        for c in self.FORBIDDEN_CHARACTERS:
            title = title.replace(c, '')
        return title

    def _to_markdown(self, text: str) -> str:
        """Return text with double linebreaks."""
        return text.replace('\n', '\n\n')

    def _write_file(self, filePath: str, text: str) -> str:
        """Write a single file and create a backup copy, if applicable.
        
        Positional arguments:
            filePath: str -- Path of the file to write.
            text: str -- File content.
            
        Return a success message.
        """
        backedUp = False
        if os.path.isfile(filePath):
            try:
                os.replace(filePath, f'{filePath}.bak')
                backedUp = True
            except Exception as ex:
                raise Exception(f'Error: Cannot overwrite "{os.path.normpath(filePath)}": {str(ex)}.')

        try:
            with open(filePath, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as ex:
            if backedUp:
                os.replace(f'{filePath}.bak', self.filePath)
            raise Exception(f'Error: Cannot write "{os.path.normpath(filePath)}": {str(ex)}.')

        return f'"{os.path.normpath(filePath)}" written.'

