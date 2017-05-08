import logging
import os
import re

import youtube_dl
from bottle import Bottle, run, static_file, \
                debug, request, mako_view as view, \
                mako_template as template


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
    'outtmpl': dir_path + "/"+"download/" + "%(id)s.%(ext)s",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
}


@app.post('/')
@view('index.html')
def index():
    return


@app.get('/<filepath:path>')
def static_files(filepath):
    return static_file(
        filepath,
        root=dir_path+'/'+'static/'
    )


@app.post('/download')
def download():
    """Serves mp3s for download
    """
    url = request.forms.get('url')
    url_match = regexp.match(url)
    if url_match:
        url = url_match.group()
        with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url)
        filename = info['title'] + '.mp3'
        return static_file(
            info['id'] + '.mp3',
            root=dir_path+'/'+'download/',
            download=filename
        )
    else:
        return template('index.html', {})

if __name__ == '__main__':
    run(app, reloader=True)
