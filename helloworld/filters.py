'''Define filters for Flask-specific WSGI applications.

We define the filters (i.e middleware) below in a way that wrapper application
remains a valid Flask object. 
Basically this boils down to:
    app.wsgi_app = FooMiddleware(app.wsgi_app, **config)
instead of:
    app = FooMiddleware(app, **config)
The later form is also a valid WSGi application, but loses all the extended Flask
functionality (like app.run() for debugging purposes).
''' 

import os
import flask
import logging

log1 = logging.getLogger(__name__)

def make_static_filter(global_config, document_root, cache_max_age=None):
    
    from paste.urlparser import make_static
    from paste.cascade import Cascade
    
    document_root = os.path.realpath(document_root)
    if not os.access(document_root, os.X_OK | os.R_OK):
        raise ValueError(
            'The document-root (%s) is not accessible' % (document_root))
    
    def filter(app):
        static_app = make_static(global_config, document_root, cache_max_age)
        app.wsgi_app = Cascade([static_app, app.wsgi_app])
        return app
    return filter

def make_session_filter(global_config, **config):
    '''Create a beaker session middleware.

    This filter ties Flask's session request-wide variable to the underlying
    beaker session object (beaker.session entry in WSGI environment).
    '''

    from beaker.middleware import SessionMiddleware
    from flask.sessions import SessionInterface

    class BeakerSessionInterface(SessionInterface):
        
        def save_session(self, app, session, response):
            session.save()

        def open_session(self, app, request):
            session = request.environ['beaker.session']
            return session

    def filter(app):
        app.wsgi_app = SessionMiddleware(app.wsgi_app, config)
        app.session_interface = BeakerSessionInterface()
        return app
    return filter

def make_urlmap_filter(global_config, **config):

    from paste.urlmap import URLMap
    from paste.deploy import loadapp
    
    config_file = global_config['__file__']

    # Note: The non-default applications (mapped at certain prefixes)
    # will not behave as Flask applications (will only be WSGI compatible)
    def filter(app):
        app.wsgi_app = URLMap(app.wsgi_app)
        for prefix, name in config.items():
            if not name.startswith('config:'):
                name = 'config:%s#%s' % (config_file, name)
            app.wsgi_app[prefix] = loadapp(name)
        return app
    return filter
