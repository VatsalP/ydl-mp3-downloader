import youtube_dl
from bottle import Bottle, run, static_file, debug, request


app = Bottle()
debug(True)


@app.get('/')
def index():
    return """
        Enter URL:
        <form method='post' action='/download'>
            <input type='text' placeholder='Enter url' name='url'>
            <input type="submit" value="Submit">
        </form>
        """

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

YDL_OPTS = {
    'format': 'bestaudio/best',
#    'outtmpl': "%(title)s.%(ext)s",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
}


@app.post('/download')
def download():
    url = request.forms.get('url')
    print(url)
    print(type(url))
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(url)

    filename = info['title'] + '-' + info['id'] + '.mp3'
    return static_file(filename, root=".", download=filename)

run(app, reloader=True)
