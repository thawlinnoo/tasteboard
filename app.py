from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__) #creates the app with flask
app.config["SECRET_KEY"] = "dev-secret-key"

Bootstrap5(app) #connect the Bootstrap styling

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasteboard.db" #create or use a SQLite db file


db = SQLAlchemy(app) #connect Flask app with db

class User(db.Model): #creating table in db
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_harsh = db.Column(db.String(200), nullable=False)
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

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) #Foreign keys are for actual db link

    author = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="restaurant_post")

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    restaurant_post_id = db.Column(db.Integer, db.ForeignKey("restaurant_posts.id"), nullable=False)

    author = db.relationship("User", back_populates="comments")
    restaurant_post = db.relationship("RestaurantPost", back_populates="comments")
    
    

@app.route("/") #homepage
def home():
    return render_template("index.html") #shows HTML page

if __name__ == "__main__": #to check whether the file is running directly from this file.
    app.run(debug=True) #to reload the local server every time we save the file after editing