from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
    def __repr__(self):
        return '<Title %r>' % self.title
        return '<Body %r>' % self.body


@app.route('/')
def index():
    if request.args:
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template("displaypost.html", blog=blog)
    else:
        posts = Blog.query.all()
        return render_template('blog.html', title="build-a-blog", posts=posts)
            



# @app.route('/blog', methods=['GET'])
# def blog():
    
#     return render_template('blog.html')
    
   

@app.route('/newpost', methods=['GET','POST'])
def newpost():
    if request.method == 'GET':
        return render_template("newpost.html")

    if request.method == 'POST':
        title= request.form['title']
        body=request.form['body']
        title_error = ""
        body_error =""
        
        if len(title) < 1:
            title_error = "Please enter a title"
        if len(body) < 1:
            body_error = "please type inside the body before you submit"
        else:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            post_url = "/?id=" + str(new_post.id)
            return redirect(post_url)
        
        return render_template("newpost.html", title="Add New Post", title_error=title_error, body_error=body_error)

    #return render_template('newpost.html')
# @app.route('/displaypost', methods=['GET'])
# def displaypost():
#     if request.method == 'GET':
#         blog_id = request.args.get('id')
#         blog = Blog.query.get(blog_id)

#         return render_template('displaypost.html', blog=blog)


#TODO make nav links that link to the main blog page and to add new blog page
#TODO: if blog title or body is left empty then return with an error message.
if __name__ == '__main__':
    app.run()