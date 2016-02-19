import flask
import logging
from flask import Flask, request, session
from flask import url_for, make_response, redirect, abort
from flask import render_template
import sqlalchemy

from helloworld import model

def make_app(global_config, **app_config):

    app = Flask(__name__)
    app.config.update(app_config)

    log1 = logging.getLogger(__name__)

    # Create database session factory for requests
    
    db_engine = sqlalchemy.create_engine(
        app_config.get('database.url', 'sqlite://'))
    model.Session.configure(bind=db_engine)

    # Setup application routes

    @app.route('/')
    @app.route('/index')
    def index():
        return 'Admin Area!!'
    
    return app
