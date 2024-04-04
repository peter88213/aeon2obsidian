"""Provide helper functions for Aeon Timeline 2 file operation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/aeon2nv
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import codecs
import json
import zipfile


def open_timeline(filePath):
    """Unzip the project file and read 'timeline.json'.

    Positional arguments:
        filePath -- Path of the .aeon project file to read.
        
    Return a Python object containing the timeline structure.
    Raise the "Error" exception in case of error. 
    """
    with zipfile.ZipFile(filePath, 'r') as myzip:
        jsonBytes = myzip.read('timeline.json')
        jsonStr = codecs.decode(jsonBytes, encoding='utf-8')
    if not jsonStr:
        raise ValueError('No JSON part found in timeline data.')
    jsonData = json.loads(jsonStr)
    return jsonData

