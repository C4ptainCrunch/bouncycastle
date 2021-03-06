#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *
from path import path
import time
from subprocess import check_output
from helpers import set_token_info, get_token_info

def process_url(requestpath):
    '''Processes a url into a mp3 and updates .status files.
    Deletes .request at the end of the processing phase'''

    token = requestpath.namebase
    url = requestpath.text()

    print 'Converting {}'.format(url) # Usefull to debug

    set_token_info(token, status='wip')

    try:
        audiopath = PROCESSING_DIR / (token + '.%(ext)s')
        title = convert_file(url, audiopath)
        print 'Done.' # Usefull to debug
        set_token_info(token, status='done', title=title)

    except:
        print 'Error during convert.'
        set_token_info(token, status='error')

    finally:
        requestpath.unlink() # Delete .request file


def convert_file(url, path):
    '''Converts a url to a mp3 into `path` and returns the song title'''

    check_output(CONVERT_CMD.format(path=path, url=url), shell=True)

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

