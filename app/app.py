from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import false
from app.forms import LoginForm
import requests
from flask_ckeditor import CKEditor

from config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
ckeditor = CKEditor(app)

#ui routes
@app.route("/login",methods=['POST', 'GET'])
def loginUser():
    from models import User

    form = LoginForm()  
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()

            if not user:
                flash("That email does not exist, please try again.")
                return redirect(url_for('login'))
            elif not check_password_hash(user.password, password):
                flash('Password incorrect, please try again.')
                return redirect(url_for('login'))
            else:
                login_user(user)
                return redirect(url_for('get_comments'))
        return redirect(url_for('success', name = user))

    return render_template("login.html",form=form)

@app.route("/signup")
def registerUser():
    return render_template("register.html")

#blog routes 
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/one-post")
def view_one_post():
    return render_template("post.html")

@app.route("/blog/create")
def create_post():
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

