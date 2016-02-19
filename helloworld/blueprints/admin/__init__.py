from flask import Blueprint
from flask import render_template

blueprint = Blueprint('admin', __name__, template_folder='templates')

# Note: 
# The templates provided at the application level have precedence over the
# blueprint level. So, consider blueprint-level resources as reasonable defaults.

@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('admin/index.html')

@blueprint.route('/index1')
def index1():
    return render_template('admin/index1.html')
