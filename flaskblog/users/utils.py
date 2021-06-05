import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flask import current_app
from flaskblog import mail


def save_pic(form_picture):
    """
    Fn for saving the user uploaded profile picture to our file system
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # Filename is an attribute of FileField object
    pic_filename = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_filename)
    # Store in that path after resizing, but we haven't yet updates user pic in db. We do not bring it into this function

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)

    return pic_filename


def remove_old_pic(current_pic):
    # print(current_pic)
    current_pic_path = os.path.join(current_app.root_path, 'static/profile_pics', current_pic)
    if os.path.exists(current_pic_path):
        os.remove(current_pic_path)


# Fn to send mail to user, given user object
def send_reset_link(user):
    # user object , not the user class
    token = user.provide_reset_token()
    msg = Message(subject='Password Reset Requested',
                  sender='noreply@BorntoBlog.com',
                  recipients=[user.email])
    # {url_for} is used, since it is inside an f string
    # _external=True is for the url to be absolute and not relative
    msg.body = f"""To reset your password, visit the link below:
{url_for('users.reset_password', token=token, _external=True)}

If you did not request password reset, please ignore this message.No changes will be made
"""
    mail.send(msg)
