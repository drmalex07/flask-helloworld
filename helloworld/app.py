#!/usr/bin/env python

import json
import flask
import urllib
import logging
from urllib import urlencode
from flask import url_for, request, make_response, redirect
from flask import render_template
from beaker.middleware import SessionMiddleware


from helloworld import config

app = flask.Flask(__name__)

log = logging.getLogger(__name__)

#
# Setup application routes
#

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
        k: str(v) for k, v in request.environ.items()
    })
    resp = make_response(environ_dump, 200)
    resp.headers['content-type'] = 'application/json; charset=utf-8'
    return resp

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name='nobody'):
    log.info('Rendering template hello.html')
    return render_template('hello.html', name=name)

#
# Setup middleware
#

app_config = config['app']

app.wsgi_app = SessionMiddleware(app.wsgi_app, app_config)
