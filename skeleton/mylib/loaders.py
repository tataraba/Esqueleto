from importlib import import_module
from inspect import isclass
from os import walk
from os.path import abspath, basename, dirname, join
from sys import modules
from pathlib import Path

from flask_classful import FlaskView
from flask_sqlalchemy import Model

__all__ = ('get_models', 'load_models')

# define main project path/module name
PROJ_DIR = Path(__file__).resolve().parents[1]
APP_MODULE = PROJ_DIR.name

def get_modules(module):
    """Returns all .py modules in given file_dir that are not __init__."""
    file_dir = PROJ_DIR / module
    
    mods = [f for f in list(file_dir.rglob('*.py')) if not f.stem == '__init__.']
    for filepath in mods:
        idx = (filepath.parts).index(APP_MODULE)
        yield ('.'.join(filepath.parts[idx:])[0:-3])
    
def dynamic_loader(module, compare):
    """Iterates over all .py files in `module` directory, finding all classes that
    match `compare` function.
    Other classes/objects in the module directory will be ignored.

    Returns unique items found.
    """
    items = [] 
    for mod in get_modules(module):
        module = import_module(mod)
        if hasattr(module, '__all__'):
            objs = [getattr(module, obj) for obj in module.__all__]
            items += [o for o in objs if compare(o) and o not in items]
    return items

def get_models():
    """Dynamic model finder."""
    return dynamic_loader('models', is_model)

def is_model(item):
    """Determines if `item` is a `db.Model`."""
    return isclass(item) and issubclass(item, Model) and not item.__ignore__()

def load_models():
    """Load application models for management script & app availability."""
    for model in get_models():
        setattr(modules[__name__], model.__name__, model)

def get_views():
    """Dynamic view finder."""
    return dynamic_loader('views', is_view)

def is_view(item):
    """Determine if `item` is a `FlaskView` subclass
    (because we don't want to register `FlaskView` itself).
    """
    return item is not FlaskView and isclass(item) and issubclass(item, FlaskView) # and not item.__ignore__()