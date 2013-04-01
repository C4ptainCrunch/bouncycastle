#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy
from cherrypy.lib.static import serve_file

import json

from path import path
from urlparse import urlparse
from hashlib import md5

from config import *
from helpers import get_html, token_status, isToken


class Zoidberg(object):

    @cherrypy.expose
    def index(self):
        '''Index page. Just shows a form and shit'''
        return get_html('base.tpl', filecontent='index.tpl')


    @cherrypy.expose
    def wait(self, token):
        '''Shows a waiting page containing the token in a hidden field'''
        return get_html('base.tpl', filecontent='wait.tpl', content=token)


    @cherrypy.expose
    def add(self, url):
        '''Adds url to the convert queue if it is a valid url.
        Otherwise returns as 401'''

        o = urlparse(url)
        if not o.netloc in ALLOWED_DOMAINS:
            raise cherrypy.HTTPError(401, 'host not supported')

        token = md5(url).hexdigest()
        requestfile = PROCESSING_DIR / (token + '.request')
        requestfile.write_text(url)

        raise cherrypy.HTTPRedirect("/wait?token={}".format(token), 301)


    @cherrypy.expose
    def status(self, token):
        if isToken(token):
            status = token_status(token)
            if status == 'Unknown':
                raise cherrypy.HTTPError(404, 'No corresponding token')
            else:
                return status
        else:
            raise cherrypy.HTTPError(401, 'Invalid token')


    @cherrypy.expose
    def download(self, token):
        if not isToken(token):
            raise cherrypy.HTTPError(401, 'Invalid token')

        filepath = PROCESSING_DIR / (token + '.mp3')
        if not filepath.exists():
            raise cherrypy.HTTPError(404, 'Hey ! I dont know this token !')

        titlefile = PROCESSING_DIR / (token + '.status')
        title = titlefile.text().replace('/', '_')

        serve = serve_file(filepath, "application/x-download", "attachment", title + '.mp3')
        return serve


# Serve on localhost and be kind, serve static files to
CHERRY_CONFIG = {
    'global' :
    {
        'server.socket_host' : '127.0.0.1',
        'server.socket_port' : CHERRY_PORT,
        'server.logToScreen' : True,
    },
    '/static' :
    {
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : CHERRY_STATICFILES,
    }
}

# Just run this fuck'in webserver !
cherrypy.quickstart(root=Zoidberg(), config=CHERRY_CONFIG)
