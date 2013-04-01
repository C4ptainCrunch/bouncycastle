#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *
from path import path
import time
import subprocess
from subprocess import check_output

def process_url(requestpath):
    '''Processes a url into a mp3 and updates .status files.
    Deletes .request at the end of the processing phase'''

    token = requestpath.namebase
    url = requestpath.text()

    print 'Converting {}'.format(url) # Usefull to debug

    statusfile = PROCESSING_DIR/(token+'.status')
    statusfile.write_text('Wip')

    try:
        audiopath = PROCESSING_DIR/(token+'.audio')
        title = convert_file(url,audiopath)
        print 'Done.' # Usefull to debug
        statusfile.write_text(title)

    except:
        print 'Error during convert.'
        statusfile.write_text('Error')

    finally:
        requestpath.unlink() # Delete .request file


def convert_file(url,path):
    '''Converts a url to a mp3 into `path` and returns the song title'''

    check_output(CONVERT_CMD.format(path=path,url=url), shell=True)

    # Return the title of the song
    return check_output(TITLE_CMD.format(url), shell=True).strip()

try:
    while True :
        files = PROCESSING_DIR.files('*.request')
        if len(files) > 0:
            process_url(files[0])
        time.sleep(2)

except KeyboardInterrupt:
    print '\nMy work here is done. Goodbye old friend.\n'

