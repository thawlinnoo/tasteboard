# Database Design

## User

- id
- name
- email
- password_hash
- is_admin

## RestaurantPost

- id
- name
- city
- image_url
- rating
- review
- date_posted
- user_id

## Comment

- id
- text
- date_posted
- user_id
- restaurant_post_id

## Relationships

- One user can create many restaurant posts.
- One user can create many comments.
- One restaurant post can have many comments.
- Each comment belongs to one user and one restaurant post.
