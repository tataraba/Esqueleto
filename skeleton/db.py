from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import force_auto_coercion

from skeleton.mylib.loaders import load_models

__all__ = ('db', 'init_db')

# Global DB object (imported by models & views & everything else)
db = SQLAlchemy()
# support importing a functioning session query
query = db.session.query

def init_db(app=None, db=None):
    """Initializes the global database object used by the app."""
    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
      force_auto_coercion()
      load_models()
      db.init_app(app)
    else:
        raise ValueError('Cannot init DB without db and app objects.')