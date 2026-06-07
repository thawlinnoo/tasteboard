from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from datetime import datetime, timezone



app = Flask(__name__) #creates the flask app object nad store it in variable app 
app.config["SECRET_KEY"] = "dev-secret-key"

Bootstrap5(app) #connect the Bootstrap styling

login_manager = LoginManager() #create login manager object and connect it with flask app
login_manager.init_app(app) 

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasteboard.db" #create or use a SQLalchemy db object and connect it to flask app


db = SQLAlchemy(app) #connect Flask app with db

#--------------------------------

# table blueprints classes 
class User(UserMixin, db.Model): #creating blueprints for tables, python models that describe the db tables. UserMixin allow flask to use some methods, especially we need to get the user_id once the user logged in. so UserMixin allow to get user_id from this class and use it in flask-login.
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    posts = db.relationship("RestaurantPost", back_populates="author") #relationships are python shortcut to access linked data between tables in code
    comments = db.relationship("Comment", back_populates="author")


class RestaurantPost(db.Model):
    __tablename__ = "restaurant_posts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) #use lambda to avoid taking time when the app start, we want to take time only when user make comment

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) #Foreign keys are the columns in db tables that connect to each other

    author = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="restaurant_post", cascade="all, delete-orphan") #cascade="all, delete-orphan" is used to delete the child as well when we delete the parents, here if the post is deleted then the comments also need to be deleted

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    restaurant_post_id = db.Column(db.Integer, db.ForeignKey("restaurant_posts.id"), nullable=False)

    author = db.relationship("User", back_populates="comments")
    restaurant_post = db.relationship("RestaurantPost", back_populates="comments")

#-----------------------
  

with app.app_context(): #using app_context method, create tables in db by using all the db.model classes set in flask app
    db.create_all()

@login_manager.user_loader #after the flask-login saved the logged_in user_id by using UserMixin, it finds and get the whole user object from database by using user_loader, especially when user refresh page or load another page or app need to used saved user_id to know who is currently logged in, flask-login already saved the logged_in user's id in session
def load_user(user_id):
    return User.query.get(int(user_id))


#---------------------------

#form blueprints
class RegisterForm(FlaskForm): #create the blueprint of the form
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
    
class RestaurantPostForm(FlaskForm):
    name = StringField("Restaurant Name", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    image_url = StringField("Put the Image URL address here", validators=[DataRequired()])
    rating = FloatField("Rating out of 5", validators=[DataRequired(), NumberRange(min=0, max=5)])
    review = TextAreaField("Review", validators=[DataRequired()])
    submit = SubmitField("Post")

class CommentForm(FlaskForm):
    text = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Comment")


#----------------------------


#routes  

@app.route("/") #homepage, connect url / to function below
def home():
    posts = RestaurantPost.query.order_by(RestaurantPost.date_posted.desc()).all() #load all the posts from db ordered by desc date and put into variable posts, 
    comment_form = CommentForm() 
    return render_template("index.html", posts=posts, comment_form=comment_form) #flask load index.html and process jinja codes inside it and return as html response and show in web browser

@app.route("/register", methods=["GET", "POST"]) #post method here is to receive the data send from html
def register():
    form = RegisterForm() #create the from object with the RegisterForm blueprint class

    if form.validate_on_submit(): #check if user inserted form pass the validation or not
        existing_user = User.query.filter_by(email=form.email.data).first() #check whether the user inserted email is already registered in db or not

        if existing_user:
            flash("Email already registered. Please log in instead.")
            return redirect(url_for("register"))
        
        password_hash = generate_password_hash(form.password.data) #hash the password that user inserted in form
        
        if User.query.count() == 0: #check if it is the first ever user registered in the db, because the first registered id will become admin
            is_first_user = True
        else:
            is_first_user = False


        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=password_hash,
            is_admin=is_first_user

        )

        db.session.add(new_user) #add this new user into db
        db.session.commit() #save changes

        flash("Account created successfully.")
        return redirect(url_for("home"))
    
    return render_template("register.html", form=form) 

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("No account found with that email.")
            return redirect(url_for("Login"))
        
        if not check_password_hash(user.password_hash, form.password.data): #automatically switch user's input password in form into hash format to compare with the one saved in db
            flash("Incorrect password.")
            return redirect(url_for("login"))
        
        login_user(user)
        flash("Logged in successfully.")
        return redirect(url_for("home"))
    
    return render_template("login.html", form=form)

@app.route("/logout") #after log out, flask-login forget logged_in user_id from session
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for("home"))

@app.route("/posts/new", methods=["GET", "POST"])
@login_required 
def new_post():

    form = RestaurantPostForm()

    if form.validate_on_submit():
        post = RestaurantPost(
            name=form.name.data,
            city=form.city.data,
            image_url=form.image_url.data,
            rating=form.rating.data,
            review=form.review.data,
            user_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()

        flash("Restaurant post created successfully.")
        return redirect(url_for("home"))

    return render_template("new_post.html", form=form)

@app.route("/posts/<int:post_id>/comments", methods=["GET", "POST"]) #"<int:post_id>"get the post_id that user write comment on, post_id will be get from index.html
@login_required #it checks if user is logged in or not
def add_comment(post_id):

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            user_id=current_user.id,
            restaurant_post_id=post_id
        )
        db.session.add(comment)
        db.session.commit()

        flash("Comment added successfully")
    return redirect(url_for("home"))

@app.route("/posts/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = RestaurantPost.query.get_or_404(post_id) #get_or_404 will return error 404 if the id is not found
    

    if current_user.id != post.user_id and not current_user.is_admin:
        flash("You do not have permission to delete this post.")
        return redirect(url_for("home"))

    db.session.delete(post)
    db.session.commit()

    flash("Post deleted successfully.")
    return redirect(url_for("home"))

@app.route("/comments/<int:comment_id>/delete", methods=["GET", "POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)


    if current_user.id != comment.user_id and not current_user.is_admin:
        flash("You do not have permission to delete this comment.")
        return redirect(url_for("home"))

    db.session.delete(comment)
    db.session.commit()

    flash("Comment deleted successfully.")
    return redirect(url_for("home"))








if __name__ == "__main__": #to check whether the file is running directly from this file.
    app.run(debug=True) #to reload the local server every time we save the file after editing