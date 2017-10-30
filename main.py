from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'S28c2B&4mOX!'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password
    # def __repr__(self):
    #      return '<Title %r>' % self.title
    #      return '<Body %r>' % self.body

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','index','blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

# @app.route('/singleUser')
# def renderuserpage():
#     if request.args.get('user'):
#        user_id =request.args.get ('user')
#        user = User.query.get(user_id)
#        posts = Blog.query.filter_by(owner=user).all()
#        return render_template('singleUser.html', posts=posts, user=user)

@app.route('/blog')
def blog():   
    if request.args.get('user'):
        user_id = request.args.get('user')
        user = User.query.get(user_id)
        posts = Blog.query.filter_by(owner=user).all()
        return render_template('singleUser.html', posts=posts, user=user)
    elif request.args.get('id'):
        blog_id = request.args.get('id')
        blog = Blog.query.get(blog_id)
        return render_template("displaypost.html", blog=blog)
    else:
        posts = Blog.query.all()
        return render_template('blog.html', title="build-a-blog", posts=posts)

# @app.route('/blog')
# def users(): 
#     if request.args:
#         user_id = request.args.get('id')
#         user = User.query.get(user_id)
#         return render_template("singleUser.html", user=user)
#     else:
#         users = User.query.all()
#         return render_template('index.html', title="blogz", users=users)

@app.route('/')
def index(): 
    users = User.query.all()
    return render_template('index.html', title="blogz", users=users)  

@app.route('/newpost', methods=['GET','POST'])
def newpost():
    if request.method == 'GET':
        return render_template("newpost.html")

    if request.method == 'POST':
        title= request.form['title']
        body=request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        title_error = ""
        body_error =""
        
        if len(title) < 1:
            title_error = "Please enter a title"
        if len(body) < 1:
            body_error = "please type inside the body before you submit"
        else:
            new_post = Blog(title, body, owner)
            db.session.add(new_post)
            db.session.commit()
            post_url = "blog?id=" + str(new_post.id)
            return redirect(post_url)
        
        return render_template("newpost.html", title="Add New Post", title_error=title_error, body_error=body_error)


@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        user_error = ""
        password_error =""
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')

        else:
            flash("username does not exist or the password is incorrect", "error")
            return redirect('/login')

    return render_template("login.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        #TODO - validate user data
        # if len(username) < 0:
        #     flash("One or more fields is blank")
        #     return redirect('/signup')
        # if len(password) < 0:
        #     flash("One or more fields is blank")
        #     return redirect('/signup')
        # if len(verify) < 0:
        #     flash("One or more fields is blank")
        #     return redirect('/signup')
        
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            if len(username) < 1:
                flash("One or more fields is blank", "error")
                return redirect('/signup')
            elif len(password) < 1:
                flash("One or more fields is blank", "error")
                return redirect('/signup')
            elif len(verify) < 1:
                flash("One or more fields is blank", "error")
                return redirect('/signup')
            elif str(verify) != str(password):
                flash("Your passwords don't match", "error")
            else:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
       
        else:
            #TODO- say they exist
            flash("That username already exists", "error")
            return redirect('/signup')

    return render_template("signup.html")
@app.route('/logout')
def logout():
    del session['username']
    flash("You've logged out")
    return redirect('/')

    #return render_template('newpost.html')
# @app.route('/displaypost', methods=['GET'])
# def displaypost():
#     if request.method == 'GET':
#         blog_id = request.args.get('id')
#         blog = Blog.query.get(blog_id)

#         return render_template('displaypost.html', blog=blog)


#TODO make nav links that link to the main blog page and to add new blog page
#TODO: if blog title or body is left empty then return with an error message.
if __name__=='__main__':
    app.run()