import logging
import os
import re

import youtube_dl
from bottle import Bottle, run, static_file, \
                request, mako_view as view


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
logging.basicConfig(filename='ze.log', level=logging.DEBUG)
app = Bottle()
# regex for youtube links
regexp = re.compile(r"(?:youtube\.com\/\S*(?:(?:\/e(?:mbed))?\/|watch\?(?:\S*?&?v\=))|youtu\.be\/)([a-zA-Z0-9_-]{6,11})")


class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        logging.warning("Warning Message: {}".format(msg))

    def error(self, msg):
        logging.error("Error Message: {}".format(msg))


YDL_OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': dir_path + "/"+"static/download/" + "%(id)s.%(ext)s",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
}


@app.get('/<filepath:path>')
def static_files(filepath):
    if 'download' in filepath:
        filepath += '.mp3'
    return static_file(
        filepath,
        root=dir_path+'/'+'static/'
    )


"""
@app.get('/download/<filepath:path>')
def download(filepath):
    print(filepath)
    return static_file(
            filepath,
            root=dir_path+'/'+'download/'
        )
"""


@app.get('/')
@view('index.html')
def index():
    return {
        'error': False,
        'download': False,
    }


@app.post('/')
@view('index.html')
def index():
    """Serves mp3s for download
    """
    url = request.forms.get('url')
    url_match = regexp.search(url)
    if url_match:
        url = url_match.group()
        with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url)
        return {
            'error': False,
            'download': True,
            'link': info['id'],
            'dwname': info['title'] + '.mp3',
        }
    else:
        return {'error': True}


if __name__ == '__main__':
    run(app, reloader=True)
