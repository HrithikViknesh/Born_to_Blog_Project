from flask import Blueprint
import time
from flask import (flash, render_template, url_for,
                   redirect, request)
from flaskblog import db, bcrypt
from flaskblog.users.forms import (LoginForm,
                                   RegistrationForm,
                                   ResetPasswordForm,
                                   RequestResetForm,
                                   UpdateAccountForm)
from flaskblog.models import User, Post
from flask_login import (login_user, current_user,
                         logout_user, login_required)
from flaskblog.users.utils import send_reset_link, save_pic, remove_old_pic

# Same as init a Flask App
users = Blueprint('users', __name__)


# We will no longer use the global 'app' variable
@users.route('/register',
             methods=["GET", "POST"])  # bacause the form posts the values entered onto the same page(same url)
def register():
    # Curb attempts to 'Register even after successful Login'
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():  # We check database errors too during form defn apart from the usual length,unique checks
        # hash the password and store in db
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        # Inform user of success/failure in creating account
        flash(f'Your account has been created. You can Log In now!', 'success')
        return redirect(url_for('users.login'))
    return render_template("register.html", title='Register', form=form)


@users.route('/login', methods=["POST", "GET"])
def login():
    # Curb attempts to Log In again, while already logged in and active
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # But if using Login page just to access Account page, straight away redirect to Accounts page
            next_page = request.args.get('next')
            if next_page:
                return redirect(url_for('users.account'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful.Please check if you have entered the correct credentials.', 'danger')
    return render_template("login.html", title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Account Page must be accessible only if user is logged in, so use suitable decorator
@users.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_pic(form.picture.data)
            old_pic = current_user.image_file
            current_user.image_file = pic_file
            if old_pic != 'default.jpg':
                remove_old_pic(old_pic)
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash("Account details updated successfully!", 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':  # To automatically fill user's current credentials
        # We used 'GET' method because when form is unsubmitted, it is in the default GET state.Only when submit button is clicked , a POST request is made
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static',
                         filename=f'profile_pics/{current_user.image_file}')  # Image file is a variable(field) in User db model
    return render_template('account.html', title='Account', form=form,
                           image_file=image_file)


# Route to view all posts by a specific user
@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # Def val is 1
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user). \
        order_by(Post.date_posted.desc()). \
        paginate(per_page=4, page=page)

    return render_template("user_posts.html", posts=posts, user=user)


# Route to enter mail address and request password reset
@users.route('/request_reset', methods=['POST', 'GET'])
def request_reset():
    # if User must be logged out in order to reset their password
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    """
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            send_reset_link(user)
        else:
            time.sleep(5)  # To make process time similar to actually sending an email
        flash(
            'If an account with this email address existed, an email with instructions to reset your password will have been sent.Please check your inbox and also the spam folder',
            'info')
        return redirect(url_for('users.login'))

    return render_template("request_reset.html", title='Request Password Reset', form=form)


# Route to actually reset password by providing a new password
@users.route('/request_reset/<token>', methods=['POST', 'GET'])
def reset_password(token):
    # ifUser must be logged out in order to reset their password
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    """
    # Get the token from url and verify it using the verify fn we defined in User model
    # If verified the fn from user model gives that User object
    user = User.verify_reset_token(token=token)

    if user is None:
        flash('Token invalid or expired.', 'warning')
        # send to request reset route
        return redirect(url_for('users.request_reset'))

    form = ResetPasswordForm()
    if form.validate_on_submit():  # We check database errors too during form defn apart from the usual length,unique checks
        # hash the password and store in db
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        # Inform user of success/failure in creating account
        flash(f'Your password has been reset successfully!', 'success')
        return redirect(url_for('users.login'))
    return render_template("reset_password.html", title='Reset Password', form=form)


@users.route("/view_by_author")
@login_required
def view_by_author():
    page = request.args.get('page', 1, type=int)  # Def val is 1
    users = User.query.paginate(per_page=4, page=page)
    user_info = []
    for user in users.items:
        user_likes = 0
        user_posts = Post.query.filter_by(author=user).all()
        for user_post in user_posts:
            user_likes += user_post.likes
        user_info.append({'user': user,
                          'num_posts': len(user_posts),
                          'user_likes': user_likes})
    user_info = sorted(user_info,
                       key=lambda i: (i['user_likes'], i['num_posts']),
                       reverse=True)

    return render_template('view_all_authors.html', user_info=user_info, users=users)
