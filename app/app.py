from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, login_user, logout_user
from flask import session
import flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import false
from app.forms import LoginForm, RegisterForm
import requests
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash

from config import DevelopmentConfig
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, current_user


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
db.session.commit()
ckeditor = CKEditor(app)
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.get(user_id)

#ui routes
@app.route("/login",methods=['POST', 'GET'])
def loginUser():
    from models import User
    form = LoginForm()  
    if request.method == 'POST':
        email= request.form['Email']
        password= request.form['Password']

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("That email does not exist, please try again.","error-toast")
            return redirect(url_for('loginUser'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.',"error-toast")
            return redirect(url_for('loginUser'))
        else:
            login_user(user)
            return redirect(url_for('index'))
       

    return render_template("login.html",form=form)

@app.route("/signup",methods=('GET', 'POST'))
def registerUser():
    from models import User
    form = RegisterForm(request.form)
    if request.method == 'POST' :
       
        user = User()
        user.username= request.form['Name']
        user.email= request.form['Email']
        user.set_password(request.form['Password'])
        try:
            user.save()
            flash('Thanks for registering',"success-toast")
        except:
            flash('Duplicate user exists',"error-toast")
            return redirect(url_for('registerUser'))
        return redirect(url_for('index'))
    return render_template("register.html",form=form)

@app.route("/logout")
def logout():
    logout_user()
    return render_template("index.html")
#blog routes 
@app.route("/")
def index():
    from models import Post
    posts = Post.query.all()
    return render_template("index.html", posts=posts)
@app.route("/one-post", methods=('GET', 'POST'))
def view_one_post():
    return render_template("post.html")

@app.route("/blog/create",methods=('GET', 'POST'))

def create_post():   
    from models import Post
    if request.method == 'POST' :          
        post  =  Post()
        post.title= request.form['title']
        post.subtitle= request.form['subtitle']
        post.body = request.form['content']
        post.owner_name= "kennedy"
        post.user_id= "kennedy"
        post.save()
        flash('Post Saved Success',"success-toast")
        return redirect(url_for('index'))
      
    return render_template("make-post.html", is_edit=False)
@app.route("/blog/edit")
def edit_post():
    return render_template("make-post.html", is_edit=True)

@app.route("/blog/delete")
def delete_blog():
    return "delete blog route"
@app.route("/blogs/random")
def get_random_blogs():
    random_quotes =[]
    for i in range(7):
        r = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
        random_quotes.append(r.json())
    print(random_quotes)
    # use a for loop to get atleast 10 blogs
    return render_template("random-quotes.html",posts=random_quotes)



#comments routes
@app.route("/blog/get_comments")
def get_comments():
    return "route to get blog commnets comment"
@app.route("/blog/comment")
def create_comment():
    return "route to create comment"

@app.route("/blog/update_comment")
def update_comment():
    return "route to update  comment"

@app.route("/blog/delete_comment")
def delete_comment():
    return "route to delete comment"

