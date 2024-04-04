The *aeon2obsidian* Python script extracts the items of an Aeon Timeline 2
project and generates a set of Markdown documents.

![Screenshot](Screenshots/screen01.png)

## Features

- Creates a page for each *aeonzip* event and entity. 
- Creates links between the pages according to the relationships. 
- Inserts tags, if any. 
- Inserts date/time (Gregorian date, "A.D." only) for the event-based pages. 
- Inserts duration (as set in Aeon) for the event-based pages. 
- The `__index.md` file holds the table of contents on the top level. 
- The `__events.md` file holds the table of contents of the events. 

## Requirements

- [Python](https://www.python.org/) version 3.6+.

## Download and install {#download}

[Download the latest release (version 0.99.0)](https://raw.githubusercontent.com/peter88213/aeon2obsidian/main/dist/aeon2obsidian_v0.99.0.zip)

- Unpack the zipfile and copy *aeon2obsidian.py* whereever you want.

[Changelog](changelog)

## Usage

```
aeon2obsidian.py Sourcefile

positional arguments:
  Sourcefile  The path of the .aeonzip file.

```

You can also drag an *.aeonzip* file and drop it on the *aeon2obsidian.py* icon. 

The created Markdown files are placed in a subfolder, named after the *aeon* project.

## License

This extension is distributed under the [MIT
License](http://www.opensource.org/licenses/mit-license.php).

