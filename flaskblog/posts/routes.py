from datetime import datetime
from flask import Blueprint
from flask import (flash, render_template, url_for,
                   redirect, request, abort)
from flaskblog.posts.forms import PostForm, SearchByDateForm
from flaskblog import db
from flaskblog.models import Post, User
from flask_login import login_required, current_user


posts = Blueprint('posts', __name__)


# Page to create posts
@posts.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form,
                           legend='New Post')


# A separate route for every post using variables
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)  # if not exists, 404 returned
    return render_template('post.html', title=post.title, post=post)


# A route to update or edit posts
@posts.route("/post/<int:post_id>/update", methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Only allow editing of posts by their respective authors
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form,
                           legend='Update Post')


# Route to delete posts
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Only allow deleting of posts by their respective authors
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/<int:post_id>/like", methods=['POST', 'GET'])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        abort(403)
    post_authorname = User.query.get(post.user_id).username
    if current_user.username != post_authorname and current_user.username not in post.likes_by.split('&')[1:]:
        post.likes_by = str(post.likes_by) + f'&{current_user.username}'
        post.likes += 1
        db.session.commit()
        
    return render_template('post.html', title=post.title, post=post)



@posts.route("/post/<int:post_id>/display_likes", methods=['POST', 'GET'])
@login_required
def display_likes(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('display_likes.html', post=post)




@posts.route("/post/top_posts")
def most_liked():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.likes > 0).order_by(Post.likes_by.desc()).paginate(per_page=4, page=page)
    return render_template("homepage.html", posts=posts)



@posts.route("/post/search_by_date", methods=['POST', 'GET'])
@login_required
def search_by_date():
    form = SearchByDateForm()
    if form.validate_on_submit():
        # from_day = form.from_day.data
        # from_month = form.from_month.data
        # from_year = form.from_year.data
        # to_day = form.to_day.data
        # to_month = form.to_month.data
        # to_year = form.to_year.data
        from_datetime = datetime(form.from_.data.year, form.from_.data.month, form.from_.data.day, 0, 0, 0)
        to_datetime =  datetime(form.to_.data.year, form.to_.data.month, form.to_.data.day+1, 0, 0, 0)

        page = request.args.get('page', 1, type=int)
        
        posts = Post.query.filter((Post.date_posted >= from_datetime) &
                                 (Post.date_posted <= to_datetime)).paginate(per_page=4, page=page)
        return render_template('homepage.html', posts=posts)
    return render_template('based_on_search.html',form=form)  











