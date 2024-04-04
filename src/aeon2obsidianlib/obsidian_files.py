"""Provide a base class for Markdown export from Aeon Timeline 2.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os


class ObsidianFiles:
    FORBIDDEN_CHARACTERS = ('\\', '/', ':', '*', '?', '"', '<', '>', '|')
    # set of characters that filenames cannot contain

    def __init__(self, folderPath):
        """Set the Obsidian folder."""
        self.folderPath = folderPath
        self.timeline = None

    def write(self):
        """Create a set of Markdown files in the Obsidian folder.
        
        Return a success message.
        """
        os.makedirs(self.folderPath, exist_ok=True)
        self._build_index()
        return

        for uid in self.items:
            title = self._strip_title(self.labels[uid])
            text = self._build_content(self.items[uid])
            self._write_file(f'{self.folderPath}/{title}.md', text)
        return 'Obsidian files successfully written.'

    def _build_content(self, item):
        """Return a string with the Markdown file content.
        
        Positional arguments:
            item: dictionary of Aeon item properties.
        """
        lines = []
        for uid in item:
            itemProperty = item[uid]
            if itemProperty:
                if type(itemProperty) == str:
                    lines.append(self._to_markdown(itemProperty))
                else:
                    for element in itemProperty:
                        if element in self.relationships:
                            refId, objId = self.relationships[element]
                            linkLabel = self.labels[refId]
                            link = self._strip_title(self.labels[objId])
                            line = f'- {linkLabel}: [[{link}]]'
                            lines.append(line)
                        else:
                            link = self._strip_title(self.labels.get(element, ''))
                            if link:
                                lines.append(f'[[{link}]]')
                            else:
                                lines.append(self._to_markdown(element))

        return '\n\n'.join(lines)

    def _build_index(self):
        """Create index pages."""
        mainIndexlines = []
        for typeUid in self.timeline.entitiesByType:
            entityType = f'_{self._strip_title(self.timeline.types[typeUid])}'
            mainIndexlines.append(f'- [[{entityType}]]')
            entityUidList = self.timeline.entitiesByType[typeUid]

            # Create an index file with the entities of the type.
            lines = []
            for entityUid in entityUidList:
                entityName = self.timeline.entities[entityUid].name
                lines.append(f'- [[{self._strip_title(entityName)}]]')
            text = '\n'.join(lines)
            self._write_file(f'{self.folderPath}/{entityType}.md', text)

        # Create a main index file with the types.
        text = '\n'.join(mainIndexlines)
        self._write_file(f'{self.folderPath}/__index.md', text)

    def _strip_title(self, title):
        """Return title with characters removed that must not appear in a file name."""
        for c in self.FORBIDDEN_CHARACTERS:
            title = title.replace(c, '')
        return title

    def _to_markdown(self, text):
        """Return text with double linebreaks."""
        return text.replace('\n', '\n\n')

    def _write_file(self, filePath, text):
        """Write a single file and create a backup copy, if applicable.
        
        Positional arguments:
            filePath: str -- Path of the file to write.
            text: str -- File content.
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

        # return f'"{os.path.normpath(filePath)}" written.'
        print(f'"{os.path.normpath(filePath)}" written.')

