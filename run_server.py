#! /usr/bin/env python
"""

Run WSGI server

"""
from app import app

import argparse
import subprocess
import shlex


def run_server(server, port):
    if server == 'wsgiref':
        server = AppServerWSGIRef(port, app)
    elif server == 'netius':
        server = AppServerNetius(port, app)
    elif server == 'waitress':
        server = AppServerWaitress(port, app)
    elif server =='cherrypy':
        server = AppServerCherrypy(port, app)
    elif server == 'gunicorn':
        server = AppServerGunicorn(port, 'app:app')
    elif server == 'uwsgi':
        server = AppServerUwsgi(port, 'app.py')
    else:
        print 'Unsupported server {}'.format(server)
        exit(-1)
    server.run()


class AppServerWSGIRef(object):
    """
    Python buildin uwsgiref server.
    https://docs.python.org/2/library/wsgiref.html
    """
    def __init__(self, port, app):
        self.port = port
        self.app = app

    def run(self):
        import wsgiref.simple_server
        server = wsgiref.simple_server.make_server('', self.port, self.app)
        server.serve_forever()


class AppServerNetius(object):
    """
    Netius WSGI server.
    http://netius.hive.pt/
    """
    def __init__(self, port, app):
        self.port = port
        self.app = app

    def run(self):
        import netius.servers
        server = netius.servers.WSGIServer(app=self.app)
        server.serve(host='0.0.0.0', port=self.port)


class AppServerWaitress(object):
    """
    Waitress WSGI server.
    http://docs.pylonsproject.org/projects/waitress/en/latest/
    """
    def __init__(self, port, app):
        self.port = port
        self.app = app

    def run(self):
        import waitress
        waitress.serve(self.app, port=self.port)


class AppServerCherrypy(object):
    """
    Cherrypy WSGI server.
    http://docs.cherrypy.org/
    """
    def __init__(self, port, app):
        self.port = port
        self.app = app

    def run(self):
        from cherrypy import wsgiserver
        server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', self.port), self.app)
        server.start()


class AppServerGunicorn(object):
    """
    Gunicorn WSGI server.
    http://docs.gunicorn.org
    """
    def __init__(self, port, app_name):
        self.port = port
        self.app_name = app_name

    def run(self):
        cmd = 'gunicorn -b 0.0.0.0:{} {}'.format(self.port, self.app_name)
        subprocess.check_call(shlex.split(cmd))


class AppServerUwsgi(object):
    """
    UWSGI server.
    https://uwsgi-docs.readthedocs.io
    """
    def __init__(self, port, app_name):
        self.port = port
        self.app_name = app_name

    def run(self):
        cmd = 'uwsgi --http 0.0.0.0:{} --wsgi-file {} --enable-threads'.format(self.port, self.app_name)
        subprocess.check_call(shlex.split(cmd))


def main():
    parser = argparse.ArgumentParser(description='Run WSGI server.')
    parser.add_argument('server', help='Server name.')
    parser.add_argument('port', type=int, help='Server name.')
    args = parser.parse_args()

    run_server(server=args.server, port=args.port)


if __name__ == '__main__':
    main()
