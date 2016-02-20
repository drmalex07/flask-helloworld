import json
import urllib
from urllib import urlencode
from flask import Flask, request, session, current_app
from flask import url_for, make_response, redirect, abort
from flask import render_template
import sqlalchemy

from helloworld import model
from helloworld.blueprints import (admin_blueprint, articles_blueprint)

def make_app(global_config, **app_config):

    app = Flask(__name__)
    app.config.update(app_config)

    # Create database session factory for requests
    
    db_engine = sqlalchemy.create_engine(
        app_config.get('database.url', 'sqlite://'))
    model.Session.configure(bind=db_engine)

    # Setup template context

    @app.context_processor
    def setup_template_variables():
        return dict(foo=session.get('foo'), baz='99')
    
    # Setup application routes
    
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(articles_blueprint, url_prefix='/articles')

    @app.route('/foo')
    def remember_foo():
        if not 'foo' in session:
            session['foo'] = 'bar'
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

    @app.route('/')
    @app.route('/hello')
    @app.route('/hello/<name>')
    def hello(name='nobody'):
        current_app.logger.info('Rendering template hello.html')
        return render_template('hello.html', name=name)

    return app

