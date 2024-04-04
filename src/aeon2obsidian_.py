#!/usr/bin/python3
"""Convert Aeon Timeline 2 project data to Obsidian Markdown fileset. 

usage: aeon2obsidian.py Sourcefile

positional arguments:
  Sourcefile  The path of the .aeon file.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2obsidian
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import sys
from aeon2obsidianlib.aeon2_file import Aeon2File
from aeon2obsidianlib.obsidian_files import ObsidianFiles
from aeon2obsidianlib.timeline import Timeline


def main(sourcePath):
    """Convert an .aeon source file to a set of Markdown files.
    
    Positional arguments:
        sourcePath -- str: The path of the .aeon file.
    """

    # Create an Aeon 2 file object and read the data.
    aeon2File = Aeon2File(sourcePath)
    aeon2File.timeline = Timeline()
    print(aeon2File.read())

    # Define the output directory.
    aeonDir, aeonFilename = os.path.split(sourcePath)
    projectName = os.path.splitext(aeonFilename)[0]
    obsidianFolder = os.path.join(aeonDir, projectName)

    # Create an Obsidian fileset object and write the data.
    obsidianFiles = ObsidianFiles(obsidianFolder)
    obsidianFiles.timeline = aeon2File.timeline
    print(obsidianFiles.write())


if __name__ == '__main__':
    main(sys.argv[1])
