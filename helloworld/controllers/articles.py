from flask import request
from flask import redirect, url_for
from flask import render_template
from flask import current_app

from helloworld import model

class ArticlesController(object):

    def __init__(self):
        self.app_config = current_app.config

    def list_articles(self):
        db_session = model.Session()
        articles = db_session.query(model.Article)\
            .order_by(model.Article.posted_at.desc()).all()
        return render_template('articles.html', articles=articles)
    
    def show_article(self, aid):
        db_session = model.Session()
        article = db_session.query(model.Article).get(aid)
        return render_template('article.html', article=article)
   
    def save_new_article(self):
        redirect_url = None 
        if 'cancel' in request.form:
            redirect_url = url_for('list_articles')
        else:
            db_session = model.Session()
            article = model.Article(
                title=request.form['title'], body=request.form['body'])
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
  
    def show_new_article(self):
        return render_template('new-article.html')

