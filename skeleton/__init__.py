from flask import Flask
from os.path import abspath, dirname, isfile, join

from skeleton.db import db, init_db

def create_app(config_file=None):
    """Default application factory.

    Default usage:
        app = create_app()

    Usage with config file:
        app = create_app('/path/to/config.yml')

    If config_file is not provided, will look for default
    config expected at '<proj_root>/config/config.yml'.
    Returns Flask app object.
    Raises EnvironmentError if config_file cannot be found.
    """

    current_dir = dirname(abspath(__file__))
    if config_file is None:
        # Use default config file location
        config_file = abspath(join(current_dir, '../config.py'))
    else:
        # Use the user defined config file
        config_file = abspath(config_file)
    if not isfile(config_file):
        raise EnvironmentError('App config file does not exist at %s' % config_file)

    # Initialize the app
    app = Flask(__name__, instance_relative_config=False)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProdConfig")
    else:
        app.config.from_object("config.DevConfig")
    
    # Initialize db (register all models through loader function in db.py)
    init_db(app, db)
  
    # Initialize views (register all views through loader function in views/_init_.py)
    from skeleton.views import init_views
    init_views(app)

    return app