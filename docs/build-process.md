# Build Process

## Step 1: Created Flask App Skeleton

Created the basic project structure for the Flask application.

Files/folders created:
- app.py
- templates/
- static/
- requirements.txt
- docs/

## Step 2: Set Up Base Layout

Created `base.html` as the main layout file.

This file contains the shared HTML structure used by other pages, including:
- HTML head
- Bootstrap CSS
- custom CSS link
- content block

## Step 3: Created Initial Home Page

Created `index.html` and extended the layout from `base.html`.

The homepage currently shows the initial TasteBoard welcome content.

## Step 4: Created Home Page Route

Created the `/` route in `app.py`.

This route renders `index.html` when the user visits the homepage.

## Step 5: Connected Flask App with Database

Added Flask-SQLAlchemy to the project.

Configured the SQLite database using:

python
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasteboard.db"
db = SQLAlchemy(app)

## Step 6: Created Database Tables

Imported the `app` and `db` objects from `app.py` in the Python shell.

Used `app.app_context()` to give SQLAlchemy access to the Flask app configuration, then ran `db.create_all()` to create the real SQLite database tables from the model classes.