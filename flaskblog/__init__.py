from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config




# Define DB
db = SQLAlchemy()

# Hash passwords
bcrypt = Bcrypt()



login_manager = LoginManager()
# Instructing the login_required decorator function about where the route for Login is located
login_manager.login_view = 'users.login'                # Fn name of login route
# This was previously just login, before introducing blueprints
# Formatting the messages by Login Manager
login_manager.login_message_category = 'info'     # Bootstrap Class



mail = Mail()

# (Before blueprint)Import routes at the bottom to avoid circular imports
# from flaskblog.app import routes



"""
Functionize app instance creation so that
multiple instances of the app can be created,
based on different configs during dev and deployment.

Also since according to Flask documentation, a single extension 
such as db or a mail, can be 
used independently for multiple apps,
so we shall keep the extension creations outside 
                        the app creation function 
and independent of the 'app' variable 
"""
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    # Attaching the app to general extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Import Blueprint onjects
    from flaskblog.users.routes import users  # Blueprint object
    from flaskblog.posts.routes import posts  # Blueprint object
    from flaskblog.main.routes import main  # Blueprint object
    from flaskblog.errors.handlers import errors

    # Register the imported blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app


"""
Now that we have functionized app creation,
there is no global variable called 'app',
But some of our files try to import it.
So we use the flask import called current_app
"""









