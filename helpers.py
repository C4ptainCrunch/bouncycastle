from path import path
from config import *
import json
import cherrypy

def get_html(template, filecontent=None, content=None):
    '''Really dumb "templating" system. Give a base template in template
    an inner template in filecontent and some real content in content.
    get_html() will put content in filecontent then filecontent in template.
    If filecontent is None, get_html() will put content in template directly'''

    if filecontent is None:
        return open(CHERRY_TEMPLATESDIR / template).read().format(content)
    else:
        fill = open(CHERRY_TEMPLATESDIR / filecontent).read().format(content)
        return open(CHERRY_TEMPLATESDIR / template).read().format(fill)


def isToken(token):
    '''Cheks if token is a valid video token (aka a md5 string).'''

    if not len(token) == 32:
        return False
    if ('.' in token) or ('/' in token):
        return False
    # TODO : make a real check.
    return True


def get_token_info(token):
    '''Checks the status of the video url associated with the given token
    Will retrun : Unknown, Queued, Error, Wip or Done'''

    metapath = PROCESSING_DIR / (token + '.meta')
    if not metapath.exists():
        return False

    meta = json.loads(metapath.text())
    return meta

def init_token_info():
    '''Creates a new (for now) empty token info'''
    meta = {
    }
    return meta

def set_token_info(token,**xargs):
    '''Changes/sets all meta values (passed as named params) of the given token
    and writes to disk'''
    meta = get_token_info(token)
    if not meta:
        meta = init_token_info()

    for key in xargs:
        meta[key] = xargs[key]

    metapath = PROCESSING_DIR / (token + '.meta')
    metapath.write_text(json.dumps(meta))


def servejson(func):
    '''Decorator : sets Content-Type to application/json' and converts
    the output to json with json.dumps()'''
    def decorate(*args, **kwargs):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps(func(*args, **kwargs))
    return decorate

def post_only(func,error_str='Method not allowed. Plz send POST with the <token> param'):
    '''Decorator : allows only POST (case insensitive) http method on the funtion.
    If cherrypy.request.method != POST sends error_str'''

    def send_error(*args, **kwargs):
        return error_str

    if not cherrypy.request.method.upper() == 'POST':
        return send_error
    return func