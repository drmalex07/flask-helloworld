#!/usr/bin/env python

import json
from flask import Flask, url_for, request, make_response
from beaker.middleware import SessionMiddleware

from helloworld import config

app = Flask(__name__)

# Setup application routes

@app.route('/')
def index():
    session = request.environ['beaker.session']
    if not session.has_key('foo'):
        session['foo'] = 'bar' 
        session.save()   
        return 'foo=' + session['foo'] + " [saved]"
    else:
        return 'foo=' + session['foo']

@app.route('/environ')
def print_environ():
    environ_dump = json.dumps({
        k: repr(request.environ[k]) for k in sorted(request.environ)
    })
    resp = make_response(environ_dump, 200)
    resp.headers['content-type'] = 'application/json; charset=utf-8'
    return resp

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name='nobody'):
    return 'Hello %s' % (name)

# Setup middleware

app_config = config['app']

app.wsgi_app = SessionMiddleware(app.wsgi_app, app_config)

