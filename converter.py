#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *
from path import path
import time
import subprocess
from subprocess import check_output

def process_file(requestpath):
    url = requestpath.text()
    token = requestpath.namebase
    print 'Converting {}'.format(url)
    statusfile = PROCESSING_DIR/(token+'.status')
    statusfile.write_text('Wip')
    audiopath = PROCESSING_DIR/(token+'.audio')
    try:
        title = convert_file(url,audiopath)
        print 'Done.'
        statusfile.write_text(title)
    except:
        print 'Error during convert.'
        statusfile.write_text('Error')
    finally:
        requestpath.unlink()

def convert_file(url,path):

    title = check_output(TITLE_CMD.format(url), shell=True).strip()
    check_output(CONVERT_CMD.format(path=path,url=url), shell=True)
    return title

try:
    while True :
        files = PROCESSING_DIR.files('*.request')
        if len(files) > 0:
            process_file(files[0])
        time.sleep(2)
except KeyboardInterrupt:
    print '\nThx, bye !\n'

