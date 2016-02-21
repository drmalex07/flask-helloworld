'''
A Flask blueprint that provides actions for a repoze.who-friendlyform login.

An example configuration for the repoze.who-friendlyform plugin:

[plugin:friendlyform]
use = repoze.who.plugins.friendlyform:FriendlyFormPlugin
login_form_url= /login
login_handler_path = /handle-login
post_login_url = /logged-in
logout_handler_path = /handle-logout
post_logout_url = /logged-out
login_counter_name = n
rememberer_name = auth_tkt
charset = utf8
'''

import os
from flask import Blueprint
from flask import request
from flask import url_for, redirect
from flask import render_template as _render_template
from jinja2 import TemplateNotFound

def make_blueprint(name):
    '''Make a named blueprint'''

    def render_template(tpl_name, **context):
        '''Render template using blueprint-level fallback.
        
        Since the enclosing factory has an arbitrary name suuplied from
        the application, we cannot simply rely on the fallback mechanism
        provided by flask.render_template().  
        '''
        path = os.path.join(name, tpl_name)
        try:
            r = _render_template(path, **context)
        except TemplateNotFound as ex:
            r = _render_template(tpl_name, **context)
        return r    
        
    blueprint = Blueprint(name, __name__, template_folder='templates')
    
    @blueprint.route('/login')
    def login():
        from_url = request.args.get('came_from', '/')
        n = request.environ['repoze.who.logins']
        handler = url_for('.handle_login', came_from=from_url, n=n)
        tpl_vars = dict(login_handler=handler, came_from=from_url, login_counter=n)
        return render_template('login_form.html', **tpl_vars)

    @blueprint.route('/handle-login')
    def handle_login():
        # noop: intercepted by repoze.who-friendlyform
        return

    @blueprint.route('/logout')
    def logout():
        return redirect(url_for('.handle_logout'))

    @blueprint.route('/handle-logout')
    def handle_logout():
        # noop: intercepted by repoze.who-friendlyform
        return

    @blueprint.route('/logged-in')
    def after_login():
        '''A hook invoked after every login attempt (successfull or not)'''
        identity = request.environ.get('repoze.who.identity')
        from_url = request.args.get('came_from', '/')
        if identity:
            return redirect(from_url)
        else:
            n = request.environ['repoze.who.logins'] + 1
            login_url = url_for('.login', came_from=from_url, n=n)
            return redirect(login_url)

    @blueprint.route('/logged-out')
    def after_logout():
        '''A hook invoked after a successfull logout (i.e. "forget" action)'''
        return render_template('logged_out.html')

    return blueprint

