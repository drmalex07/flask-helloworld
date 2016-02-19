from flask import Blueprint
from flask import render_template

blueprint = Blueprint('admin', __name__)

@blueprint.route('/')
@blueprint.route('/index')
def show_index():
    return render_template('admin/index.html')
