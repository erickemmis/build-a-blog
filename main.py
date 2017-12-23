from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 
import datetime, html


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://build-a-blog:zraMN4XtTaYOvjZB@localhost:8889/build-a-blog"
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.String(280))
    post_date = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.post_date = datetime.datetime.now()


@app.route('/blog')
def blog():
    blog = Blog.query.all()

    return render_template('blog.html', blog=blog)

@app.route('/newpost', methods=["POST","GET"])
def newpost():

    if request.method == 'POST':
        valid = True
        title_error = ''
        body_error = ''

        title = request.form['title']
        body = request.form['body']

        #check if both title and body are there
        if not title:
            title_error = "Pleae fill in a title"
            valid = False
        if not body:
            body_error = "Pleae fill in a body"
            valid = False


        if valid:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')
        else: 
            return render_template('newpost.html', 
                                           title_error=title_error,
                                           body_error=body_error)


    return render_template('newpost.html')
    


if __name__ == '__main__':
    app.run()