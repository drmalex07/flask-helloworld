from flask import Blueprint
from flask import render_template, request, redirect, abort, url_for

from helloworld import model

blueprint = Blueprint('articles', __name__)

@blueprint.route('/', methods=['GET'])
def index():
    db_session = model.Session()
    articles = db_session.query(model.Article)\
        .order_by(model.Article.posted_at.desc()).all()
    return render_template('articles/index.html', articles=articles)

@blueprint.route('/<int:aid>')
def show(aid):
    db_session = model.Session()
    article = db_session.query(model.Article).get(aid)
    return render_template('articles/show.html', article=article)

@blueprint.route('/new', methods=['POST'])
def create():
    redirect_url = None 
    if 'cancel' in request.form:
        redirect_url = url_for('.index')
    else:
        db_session = model.Session()
        article = model.Article(
            title=request.form['title'], body=request.form['body'])
        try:
            db_session.add(article)
            db_session.commit()
            redirect_url = url_for('.index')
        except:
            db_session.abort()
        finally:
            db_session.close()
    if redirect_url:
        return redirect(redirect_url)
    else:
        abort(500)

@blueprint.route('/new', methods=['GET'])
def edit_new():
    return render_template('articles/new.html')

