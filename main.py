import os
import socket
import bottle
from bottle import run, ServerAdapter, static_file, template, get
import datetime

import logging

logger = logging.getLogger(__name__)

@get('/')
def index():
    return template('index', {})

@get('/flashcards')
def flashcards():
    flashcards = []
    path = os.path.join(os.path.dirname(__file__), 'static/flashcards')
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path) and filename.endswith('.png'):
            answer = filename.replace('_', ' ')[:-4]
            image = '/static/flashcards/' + filename
            flashcards.append({'image': image, 'answer': answer})
    return {'flashcards': flashcards}

class GEventServer(ServerAdapter):
    """ Fast HTTP Server """
    def run(self, handler):
        from gevent.wsgi import WSGIServer
        WSGIServer((self.host, self.port), handler).serve_forever()

static_file_path = os.path.join(os.path.dirname(__file__), 'static')

if __name__ == "__main__":
    @get('/static/<filename:path>')
    def serveStatic(filename):
        response = static_file(filename, root=static_file_path)
        response.set_header('Cache-Control', 'max-age=0')
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=0)
        response.set_header('Expires', expires.strftime('%a, %d %b %Y %H:00:00 GMT'))
        return response

    bottle.debug(True)
    host = socket.gethostbyname(socket.gethostname())
    run(server=GEventServer, host=host, port=8000, reloader=True)
