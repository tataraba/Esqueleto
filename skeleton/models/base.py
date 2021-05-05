
# -*- coding: utf-8 -*-

from arrow import utcnow
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table
from sqlalchemy_utils import ArrowType

from skeleton.db import db
from .mixins.query import QueryMixin

__all__ = ('Model',)


class Model(db.Model, QueryMixin):
    """Abstract base class for all app models.

    Provides a `id` (for primary key) & `created_at` column to every model.

    To define models, follow this example:

        from .base import Model

        class MyModel(Model):
            # model definition
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def created_at(cls):
        return db.Column(ArrowType, default=utcnow, nullable=False, index=True)

    @property
    def class_name(self):
        """Shortcut for returning class name."""
        return unicode(self.__class__.__name__)

    @classmethod
    def __ignore__(cls):
        """Custom class attr that lets us control which models get ignored.

        We are using this because knowing whether or not we're actually dealing
        with an abstract base class is only possible late in the class's init
        lifecycle.

        This is used by the dynamic model loader to know if it should ignore.
        """
        return cls.__name__ in ('Model',)  # can add more abstract base classes here

    def __repr__(self):
        """"Returns a string representation of every object.

        Useful for logging & error reporting.
        Example:

            >>> obj = MyModel()
            >>> print obj
            MyModel.123

        Can be overridden by subclasses to customize string representation.
        """
        return u"{}.{}".format(self.class_name, self.pk)

    @declared_attr
    def __tablename__(cls):
        """Generate a __tablename__ attr for every model that does not have
        inherited tables.

        Ensures table names match the model name without needing to declare it.
        """
        if has_inherited_table(cls):
            return None
        return cls.__name__.lower()

