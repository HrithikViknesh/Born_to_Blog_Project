from flask import Blueprint, render_template


errors = Blueprint('errors', __name__)

# Error handlers are similar to App routes
"""
app.error_handler is used instead of errorhandler ,
bacause want these hanlders to be active
throughout the entire application,
not just the 'errors' blueprint
"""

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404    # 404 is the status code, which is by default 200

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
