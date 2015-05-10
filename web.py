#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy
from cherrypy.lib.static import serve_file

import json

from path import path
from urlparse import urlparse
from hashlib import md5

from config import *
from helpers import *


class Zoidberg(object):

    @cherrypy.expose
    def index(self):
        '''Index page. Just shows a form and shit'''
        return get_html('base.tpl', filecontent='index.tpl')


    @cherrypy.expose
    def wait(self, token=''):
        '''Shows a waiting page containing the token in a hidden field'''
        return get_html('base.tpl', filecontent='wait.tpl', content=token)

    @cherrypy.expose
    @jsonify
    @post_only
    def add(self, url=''):
        '''Adds url to the convert queue if it is a valid url.
        Otherwise returns as 401'''

        o = urlparse(url)
        if not o.netloc in ALLOWED_DOMAINS:
            return {'error' : 'Host not supported'}

        token = md5(url).hexdigest()
        if get_token_info(token):
            raise cherrypy.HTTPRedirect("/status?token={}".format(token), 301)

        requestfile = PROCESSING_DIR / (token + '.request')
        requestfile.write_text(url)

        set_token_info(token, url=url, status='queue')
        raise cherrypy.HTTPRedirect("/status?token={}".format(token), 301)


    @cherrypy.expose
    @jsonify
    def status(self, token=''):
        if not isToken(token):
            return {'error' : 'No token'}

        meta = get_token_info(token)
        if not meta:
            return {'error' : 'Token unknown'}

        meta.update({'token' : token})

        return meta


    @cherrypy.expose
    def download(self, token=''):
        if not isToken(token):
            return {'error' : 'Invalid token'}

        filepath = PROCESSING_DIR / (token + '.mp3')
        if not filepath.exists():
            return {'error' : 'Hey ! I dont know this token !'}

        meta = get_token_info(token)
        if not meta or not meta['title'] or not meta['status'] == 'done':
            return {'error' : 'Error... Please retry or contact admin'}

        cherrypy.response.headers.update({
            'X-Accel-Redirect'    : '/accel-download/{0}'.format(token + '.mp3'),
            'Content-Disposition' : 'attachment; filename={0}.mp3'.format(meta['title']),
            'Content-Type'        : 'application/octet-stream'
        })

    @cherrypy.expose
    def index_tpl(self):
        return (CHERRY_TEMPLATESDIR / 'index.tpl').text()

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

def application(environ, start_response):
  cherrypy.tree.mount(Zoidberg(), '/', None)
  return cherrypy.tree(environ, start_response)


if __name__ == '__main__':
    # Just run this fuck'in webserver !
    cherrypy.quickstart(root=Zoidberg(), config=CHERRY_CONFIG)

