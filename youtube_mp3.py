import logging

import youtube_dl
from bottle import Bottle, run, static_file, \
                debug, request, mako_view as view

logging.basicConfig(filename='ze.log', level=logging.DEBUG)
app = Bottle()
debug(True)


@app.get('/')
@view('index.html')
def index():
    return """
        Enter URL:
        <form method='post' action='/download'>
            <input type='text' placeholder='Enter url' name='url'>
            <input type="submit" value="Submit">
        </form>
        """


class Logger(object):
    def debug(self, msg):
        logging.debug("Message: {}".format(msg))

    def warning(self, msg):
        logging.warning("Message: {}".format(msg))

    def error(self, msg):
        logging.error("Message: {}".format(msg))

YDL_OPTS = {
    'format': 'bestaudio/best',
#   'outtmpl': "%(title)s.%(ext)s",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
}


@app.post('/download')
def download():
    """Serves mp3s for download
    """
    url = request.forms.get('url')
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(url)

    filename = info['title'] + '-' + info['id'] + '.mp3'
    return static_file(filename, root=".", download=filename)

if '__name__' == __main__:
    run(app, reloader=True)
