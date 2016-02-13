#!/usr/bin/env python

import json
import flask
import urllib
import logging
from urllib import urlencode
from flask import url_for, request, make_response, redirect, abort
from flask import render_template
import sqlalchemy

from helloworld import model

def make_app(global_config, **app_config):

    app = flask.Flask(__name__)

    log = logging.getLogger(__name__)

    # Create database session factory for requests
    
    db_engine = sqlalchemy.create_engine(
        app_config.get('database.url', 'sqlite://'))
    model.Session.configure(bind=db_engine)

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
    
    @app.route('/articles', methods=['GET'])
    def list_articles():
        db_session = model.Session()
        articles = db_session.query(model.Article)\
            .order_by(model.Article.posted_at.desc()).all()
        return render_template('articles.html', articles=articles)
    
    @app.route('/article/<aid>')
    def show_article(aid):
        db_session = model.Session()
        article = db_session.query(model.Article).get(aid)
        return render_template('article.html', article=article)
   
    @app.route('/new-article', methods=['POST'])
    def new_article():
        db_session = model.Session()
        article = model.Article(
            title=request.form['title'], body=request.form['body'])
        redirect_url = None 
        try:
            db_session.add(article)
            db_session.commit()
            redirect_url = url_for('list_articles')
        except:
            db_session.abort()
        finally:
            db_session.close()
        if redirect_url:
            return redirect(redirect_url)
        else:
            abort(500)
  
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

    # Setup middleware
    
    from beaker.middleware import SessionMiddleware
    
    app.wsgi_app = SessionMiddleware(app.wsgi_app, app_config)
    
    # Done 

    return app

