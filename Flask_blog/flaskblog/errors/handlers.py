from flask import Blueprint, render_template

errors= Blueprint('errors',__name__)

# Para manejar el error 404
@errors.app_errorhandler(404)
def error_404(error):
    # 404 is a static code
    return render_template('errors/404.html'), 404

def error_403(error):
    return render_template('errors/403.html'), 403

def error_500(error):
    return render_template('errors/500.html'), 500