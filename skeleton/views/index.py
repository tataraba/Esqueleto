from flask import url_for, redirect, render_template
from flask_classful import FlaskView, route

__all__ = ('HomepageView',)

quote = "This is greatest."

class HomepageView(FlaskView):
    route_base = '/'

    def index(self):
        return render_template('main/index.jinja2')
