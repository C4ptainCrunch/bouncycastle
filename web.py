#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy
from cherrypy.lib.static import serve_file

import json

from path import path
from urlparse import urlparse
from hashlib import md5

from config import *


class Zoidberg(object):

    @cherrypy.expose
    def index(self):
        '''Index page. Just shows a form and shit'''
        return self.get_html('base.tpl',filecontent='index.tpl')


    @cherrypy.expose
    def wait(self,token):
        '''Shows a waiting page containing the token in a hidden field'''
        return self.get_html('base.tpl',filecontent='wait.tpl',content=token)


    @cherrypy.expose
    def add(self,url):
        '''Adds url to the convert queue if it is a valid url.
        Otherwise returns as 401'''

        o = urlparse(url)
        if not o.netloc in ALLOWED_DOMAINS:
            raise cherrypy.HTTPError(401,'host not supported')

        token = md5(url).hexdigest()
        requestfile = PROCESSING_DIR/(token+'.request')
        requestfile.write_text(url)

        raise cherrypy.HTTPRedirect("/wait?token={}".format(token), 301)


    @cherrypy.expose
    def status(self,token):
        if self.isToken(token):
            status = self.token_status(token)
            if status == 'Unknown':
                raise cherrypy.HTTPError(404,'No corresponding token')
            else:
                return status
        else:
            raise cherrypy.HTTPError(401,'Invalid token')


    @cherrypy.expose
    def download(self,token):
        if not self.isToken(token):
            raise cherrypy.HTTPError(401,'Invalid token')

        filepath = PROCESSING_DIR/(token+'.mp3')
        if not filepath.exists():
            raise cherrypy.HTTPError(404,'Hey ! I dont know this token !')

        titlefile = PROCESSING_DIR/(token+'.status')
        title = titlefile.text().replace('/','_')

        serve = serve_file(filepath, "application/x-download", "attachment",title+'.mp3')
        return serve

    # ------------------ #
    # ---- Helpers ----- #
    # ------------------ #

    def get_html(self, template, filecontent=None, content=None):
        '''Really dumb "templating" system. Give a base template in template
        an inner template in filecontent and some real content in content.
        get_html() will put content in filecontent then filecontent in template.
        If filecontent is None, get_html() will put content in template directly'''

        if filecontent is None:
            return open(CHERRY_TEMPLATESDIR / template).read().format(content)
        else:
            fill = open(CHERRY_TEMPLATESDIR / filecontent).read().format(content)
            return open(CHERRY_TEMPLATESDIR / template).read().format(fill)


    def token_status(self,token):
        '''Checks the status of the video url associated with the given token
        Will retrun : Unknown, Queued, Error, Wip or Done'''

        statuspath = PROCESSING_DIR/(token+'.status')
        if not statuspath.exists():
            requestpath = PROCESSING_DIR/(token+'.request')
            if not requestpath.exists():
                return 'Unknown'
            else :
                return 'Queued'
        elif statuspath.text().strip() in ('Wip','Error'):
            return statuspath.text().strip()
        else:
            return 'Done'


    def isToken(self,token):
        '''Cheks if token is a valid video token (aka a md5 string).'''

        if not len(token) == 32:
            return False
        if ('.' in token) or ('/' in token):
            return False
        # TODO : make a real check.
        return True


# Just run this fuck'in webserver !

CHERRY_CONFIG = {
    'global':
    {
        'server.socket_host' : '127.0.0.1',
        'server.socket_port' : CHERRY_PORT,
        'server.logToScreen' : True,
    },
    '/static':
    {
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : CHERRY_STATICFILES,
    }
}
cherrypy.quickstart(root=Zoidberg(),config=CHERRY_CONFIG)
