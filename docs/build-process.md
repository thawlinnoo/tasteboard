## Created GitHub repo
Created tasteboard, cloned it to Mac, checked git status.

## Created project planning docs
Added docs like project plan, database design, build process.

## Set up Flask project skeleton
Created app.py, templates/, static/, requirements.txt.

## Created basic homepage
Made / route in app.py, base.html as shared layout, and index.html as homepage.

## Connected database
Added SQLAlchemy, SQLite database URI, and db = SQLAlchemy(app).

## Created database models
Added User, RestaurantPost, and Comment models in app.py.

## Created database tables
Used db.create_all() inside app.app_context().

## Added register system
Created RegisterForm, /register route, and register.html.

## Added login system
Added Flask-Login, LoginForm, /login route, login.html, UserMixin, and user_loader.

## Added logout system
Added /logout route and showed logout button when user is logged in.

## Added restaurant post creation
Created RestaurantPostForm, /posts/new route, and new_post.html.

## Displayed posts on homepage
Queried posts from database and looped them in index.html.

## Added comments
Created CommentForm, comment route, and displayed comments under each post.

## Added delete post/comment
Added delete routes with permission checks for owner/admin.

## Added edit post
Reused RestaurantPostForm, created /posts/<post_id>/edit, and added edit_post.html.

## Added search
Used GET search with q, request.args, and SQLAlchemy filtering by restaurant name or city.

## Started CSS cleanup
Added basic styling plan for cards, images, buttons, and layout.