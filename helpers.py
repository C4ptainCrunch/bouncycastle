from path import path
from config import *

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


def token_status(token):
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


def isToken(token):
    '''Cheks if token is a valid video token (aka a md5 string).'''

    if not len(token) == 32:
        return False
    if ('.' in token) or ('/' in token):
        return False
    # TODO : make a real check.
    return True