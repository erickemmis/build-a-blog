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

    if len(request.args) == 1:
        post_id = request.args.get('id')
        post = Blog.query.filter_by(id=post_id).first()
        return render_template('post.html', post=post)

    blog = Blog.query.order_by(Blog.post_date.desc()).all()
    return render_template('blog.html', blog=blog)

@app.route('/newpost', methods=["POST","GET"])
def newpost():
    error = {'title': '' , 'body': '' }
    blog_post = {'title': '' , 'body': ''}

    if request.method == 'POST':

        blog_post = {'title': request.form['title'],
                'body' : request.form['body']}

        #check if both title and body are there
        if not blog_post['title']:
            error['title'] = "Please fill in a title"
        if not blog_post['body']:
            error['body'] = "Please fill in a body"


        if not any(error.values()):
            #add and commit title and body in a new post if valid
            new_post = Blog(blog_post['title'], blog_post['body'])
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog?id={0}'.format(new_post.id))

    return render_template('newpost.html', error=error, blog_post=blog_post)
    

if __name__ == '__main__':
    app.run()