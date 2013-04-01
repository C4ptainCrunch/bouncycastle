from path import path

# Place where bouncy should place processing files and mp3 files
PROCESSING_DIR = path('/tmp/bouncy/')

# Root of evil
ROOT_DIR = path('/Users/nikita/Code/bouncycastle/')

# Allow conversion from following domains
ALLOWED_DOMAINS = ('www.youtube.com','youtu.be','www.dailymotion.com','soundcloud.com')

# Command used to convert the url into an mp3
CONVERT_CMD = 'youtube-dl -x --audio-format=mp3 --audio-quality=256K -o "{path}" {url}'
# Command used to get the title of the song/video
TITLE_CMD = 'youtube-dl -e {}'

# Cherrypy configuration otpions
CHERRY_PORT = 8080
CHERRY_STATICFILES = ROOT_DIR / 'static'
CHERRY_TEMPLATESDIR = ROOT_DIR

# Easy deployment should be easy
try:
    from production import *
except ImportError:
    pass

# Do not continue if PROCESSING_DIR does not exsist
if not PROCESSING_DIR.exists():
    raise Exception('PROCESSING_DIR does not exsist\n'
        + 'please create ' + PROCESSING_DIR)
