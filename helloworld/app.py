import json
from flask import Flask, request, session, current_app
from flask import url_for, make_response, redirect, abort
from flask import render_template
import sqlalchemy

from helloworld import model
from helloworld.lib.auth.helpers import (
    authenticated, get_authenticated_user)
from helloworld.blueprints import (
    who_blueprint, admin_blueprint, articles_blueprint)

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
        return dict(
	        user = get_authenticated_user(),
            foo = session.get('foo'),
            baz = '99')
    
    # Setup application routes
    
    app.register_blueprint(who_blueprint)
    
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

    @app.route('/user')
    @app.route('/user/welcome')
    @authenticated
    def user_welcome():
        logout_url = url_for('who.logout')
        return render_template('user/welcome.html', logout_url=logout_url)

    return app

