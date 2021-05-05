from flask import url_for, redirect, render_template
from flask_classful import FlaskView, route

from skeleton.mylib.loaders import get_views


def init_views(app=None):
    """Initializes application views"""
    if app is None:
        raise ValueError('Cannot init views without app object.')

    for view in get_views():
        view.register(app)
    
    register_error_handlers(app)


def register_error_handlers(app=None):
    """Register app error handlers.

    Raises an error if app is not provided.
    """
    if app is None:
        raise ValueError('Cannot register error handlers on an empty app.')

    @app.errorhandler(404)
    def error404(self):
        return render_template('errors/404.jinja2', title='Page Not Found')

    @app.errorhandler(500)
    def error500(self):
        return render_template('errors/500.jinja2', title='Server Error')