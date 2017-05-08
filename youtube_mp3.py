import logging
import os

import youtube_dl
from bottle import Bottle, run, static_file, \
                debug, request, mako_view as view


path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
logging.basicConfig(filename='ze.log', level=logging.DEBUG)
app = Bottle()


class Logger(object):
    def debug(self, msg):
        logging.debug("Message: {}".format(msg))

    def warning(self, msg):
        logging.warning("Message: {}".format(msg))

    def error(self, msg):
        logging.error("Message: {}".format(msg))


YDL_OPTS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
}


@app.get('/')
@view('index.html')
def index():
    return
    """
    return 
        Enter URL:
        <form method='post' action='/download'>
            <input type='text' placeholder='Enter url' name='url'>
            <input type="submit" value="Submit">
        </form>
    """


@app.get('/<filepath:path>')
def static_files(filepath):
    return static_file(
        filepath,
        root=dir_path+'/'+'static/'
    )


# regex for youtube links
# ^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$
# https://stackoverflow.com/questions/19377262/regex-for-youtube-url
@app.post('/download')
def download():
    """Serves mp3s for download
    """
    url = request.forms.get('url')
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(url)

    filename = info['title'] + '-' + info['id'] + '.mp3'
    return static_file(filename, root=".", download=filename)

if __name__ == '__main__':
    run(app, reloader=True)
