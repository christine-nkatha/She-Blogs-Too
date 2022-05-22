from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_sqlalchemy import SQLAlchemy

from config import DevelopmentConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#ui routes
@app.route("/ui/login")
def loginUiUser():
    render_template("login.html")
# auth routes 
@app.route("/login")
def loginUser():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_comments'))
    return render_template("login.html", form=form, current_user=current_user)
@app.route("/signup")
def registerUser():
    return "route to register user "

#blog routes 
@app.route("/")
def index():
    return "deployment success \n get all blogs route \n update test"

@app.route("/blog/create")
def create_blog():
    return "route to create new blog "

@app.route("/blog/update")
def update_blog():
    return "route to update blog"

@app.route("/blog/delete")
def delete_blog():
    return "delete blog route"
@app.route("/blogs/random")
def get_random_blogs():
    # use a for loop to get atleast 10 blogs
    return "get random blogs from external api endpoint"



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

