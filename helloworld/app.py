#!/usr/bin/env python

import json
import flask
import urllib
import logging
from urllib import urlencode
from flask import url_for, request, make_response, redirect
from flask import render_template
from beaker.middleware import SessionMiddleware
from repoze.who.config import make_middleware_with_config


from helloworld import config
from helloworld.lib.helpers import authenticated

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
@authenticated
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

@app.route('/user')
@app.route('/user/welcome')
@authenticated
def user_welcome():
    identity = request.environ.get('repoze.who.identity')
    return render_template('user/welcome.html',
        user=identity['repoze.who.userid'])

@app.route('/login')
def login():
    from_url = request.args.get('came_from', '/')
    n = request.environ['repoze.who.logins']
    handler = '/handle_login?' + urlencode({'came_from': from_url, 'n':  n})
    tpl_vars = dict(login_handler=handler, came_from=from_url, login_counter=n)
    return render_template('login_form.html', **tpl_vars)

@app.route('/logout')
def logout():
    return redirect('/handle_logout')

@app.route('/logged-in')
def after_login():
    '''A hook invoked after every login attempt (successfull or not)
    '''
    
    identity = request.environ.get('repoze.who.identity')
    from_url = request.args.get('came_from', '/')
    if identity:
        return redirect(from_url)
    else:
        n = request.environ['repoze.who.logins'] + 1
        login_url = url_for('.login', came_from=from_url, n=n)
        return redirect(login_url)

@app.route('/logged-out')
def after_logout():
    '''A hook invoked after a successfull logout (i.e. "forget" action)
    '''

    return render_template('bye.html')

#
# Setup middleware
#

app_config = config['app']

who_config_file = app_config['who.config']
who_log_file = app_config.get('who.log', 'stdout')
app.wsgi_app = make_middleware_with_config(app.wsgi_app,
    config, who_config_file, log_file=who_log_file)

app.wsgi_app = SessionMiddleware(app.wsgi_app, app_config)
