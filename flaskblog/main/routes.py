from flask import Blueprint

from flask import render_template, request, abort
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)  # Def val is 1
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=4, page=page)

    return render_template("homepage.html", posts=posts)


@main.route('/about')
def about():
    return render_template("aboutpage.html", title='About')
