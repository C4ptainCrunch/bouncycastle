from path import path
PROCESSING_DIR = path('/tmp/bouncy/')
if not PROCESSING_DIR.exists():
    raise Exception('PROCESSING_DIR does not exsist')
ALLOWED_DOMAINS = ('www.youtube.com','youtu.be','www.dailymotion.com')

CONVERT_CMD = 'youtube-dl -x --audio-format=mp3 --audio-quality=256K -o "{path}" {url}'
TITLE_CMD = 'youtube-dl -e {}'