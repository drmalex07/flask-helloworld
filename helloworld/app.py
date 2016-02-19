#!/usr/bin/env python

import json
import flask
import urllib
import logging
from urllib import urlencode
from flask import request, session
from flask import url_for, make_response, redirect, abort
from flask import render_template
import sqlalchemy

from helloworld import model

from helloworld.lib.helpers import authenticated
from helloworld.controllers import ArticlesController

def make_app(global_config, **app_config):

    app = flask.Flask(__name__)
    
    app.config.update(app_config)

    log1 = logging.getLogger(__name__)

    # Create database session factory for requests
    
    db_engine = sqlalchemy.create_engine(
        app_config.get('database.url', 'sqlite://'))
    model.Session.configure(bind=db_engine)

    # Setup template context

    @app.context_processor
    def setup_template_variables():
        identity = request.environ.get('repoze.who.identity')
        user = identity['repoze.who.userid'] if identity else None
        return dict(user=user, foo=session.get('foo'), baz='99')
    
    # Setup application routes

    @app.route('/foo')
    def remember_foo():
        if not 'foo' in session:
            session['foo'] = 'bar'
            return 'foo=' + session['foo'] + " [saved]"
        else:
            return 'foo=' + session['foo']
    
    @app.route('/articles', methods=['GET'])
    def list_articles(): 
        return ArticlesController().list_articles()
    
    @app.route('/article/<aid>')
    def show_article(aid):
        return ArticlesController().show_article(aid)
   
    @app.route('/new-article', methods=['POST'])
    def save_new_article():
       return ArticlesController().save_new_article() 
  
    @app.route('/new-article', methods=['GET'])
    def show_new_article():
       return ArticlesController().show_new_article() 
    
    @app.route('/environ')
    def print_environ():
        environ_dump = json.dumps({
            k: str(v) for k, v in request.environ.items()
        })
        resp = make_response(environ_dump, 200)
        resp.headers['content-type'] = 'application/json; charset=utf-8'
        return resp

    @app.route('/')
    @app.route('/hello')
    @app.route('/hello/<name>')
    def hello(name='nobody'):
        log1.info('Rendering template hello.html')
        return render_template('hello.html', name=name)

    @app.route('/user')
    @app.route('/user/welcome')
    @authenticated
    def user_welcome():
        return render_template('user/welcome.html')

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

    
    return app

