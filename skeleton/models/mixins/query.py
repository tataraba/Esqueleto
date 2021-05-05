# -*- coding: utf-8 -*-

from flask import abort, current_app as app
from sqlalchemy.orm.exc import ObjectDeletedError

from skeleton.db import db

__all__ = ('QueryMixin',)


class QueryMixin(object):
    """Mixin class for database queries."""

    # CRUD methods
    def save(self):
        """Save instance to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete instance."""
        db.session.delete(self)
        db.session.commit()

    # Query helpers
    @classmethod
    def exists(cls, **kwargs):
        """Checks if record matching kwargs exists in the database.

        Returns True/False.
        """
        return db.session.query(cls._and_query(kwargs).exists()).all()[0][0]

    @classmethod
    def find(cls, **kwargs):
        """Return filtered AND query results for passed in kwargs.

        Example:

            # find all instances of MyModel for first name 'John' AND last name 'Doe'
            MyModel.find(first_name='John', last_name='Doe')

        Returns result list or None.
        """
        return cls._and_query(kwargs)

    @classmethod
    def find_or(cls, **kwargs):
        """Return filtered OR query results for passed in kwargs.

        Example:

            # find all instances of MyModel for first name 'John' OR last name 'Doe'
            MyModel.find_or(first_name='John', last_name='Doe')

        Returns result list or None.
        """
        return cls._or_query(kwargs)

    @classmethod
    def find_in(cls, _or=False, **kwargs):
        """Return filtered query results for passed in attrs that match a list.

        Query defaults to an AND query. If you want an OR query, pass _or=True.
        """
        if _or:
            return cls._or_in_query(kwargs)
        else:
            return cls._and_in_query(kwargs)

    @classmethod
    def find_not_in(cls, _or=False, **kwargs):
        """Return filtered query results for passed in attrs that do not match
        a list.

        Query defaults to an AND query. If you want an OR query, pass _or=True.
        """
        if _or:
            return cls._or_not_in_query(kwargs)
        else:
            return cls._and_not_in_query(kwargs)

    @classmethod
    def find_not_null(cls, *args):
        """Return filtered query results for passed in attrs that are not None.

        Example:

            # find all instances of MyModel where email and phone != null
            MyModel.find_not_null('email', 'phone')

        NOTE: Filtering for JSON types that are not NULL does not work. JSON
        must be cast to at least text to check for a NULL value. You can verify
        this yourself in the `psql` client like so:

            # you will see null results show up
            select * from form where custom_fields is not null;

            # you will not see null results
            select * from form where custom_fields::text != 'null';

        Returns result list or None.
        """
        filters = [getattr(cls, attr) != None for attr in args]
        return cls.query.filter(*filters)

    @classmethod
    def first(cls, **kwargs):
        """Return first result for query.

        Returns instance or None.
        """
        return cls._and_query(kwargs).first()

    @classmethod
    def first_or_404(cls, **kwargs):
        """Get first item that matches kwargs or raise 404 error."""
        item = cls._and_query(kwargs).first()
        if item is None:
            return abort(404)
        else:
            return item

    @classmethod
    def get(cls, pk):
        """Get item by primary key.

        Returns instance or `None`.
        """
        return cls.query.get(pk)

    @classmethod
    def get_active_or_404(cls, pk):
        """Get item by primary key or 404 only if it is active."""
        item = cls.query.get_or_404(pk)
        if item.active:
            return item
        else:
            return abort(404)

    @classmethod
    def get_or_404(cls, pk):
        """Get item by primary key or 404."""
        return cls.query.get_or_404(pk)

    ########################################
    # Internal methods; Do not use directly
    ########################################
    @classmethod
    def _filters(cls, filters):
        """Return filter list from kwargs."""
        return [getattr(cls, attr)==filters[attr] for attr in filters]

    @classmethod
    def _filters_in(cls, filters):
        """Return IN filter list from kwargs."""
        return [getattr(cls, attr).in_(filters[attr]) for attr in filters]

    @classmethod
    def _filters_not_in(cls, filters):
        """Return NOT IN filter list from kwargs."""
        return [getattr(cls, attr).notin_(filters[attr]) for attr in filters]

    @classmethod
    def _and_query(cls, filters):
        """Execute AND query.

        Returns BaseQuery.
        """
        return cls.query.filter(db.and_(*cls._filters(filters)))

    @classmethod
    def _and_in_query(cls, filters):
        """Execute AND query.

        Returns BaseQuery.
        """
        return cls.query.filter(db.and_(*cls._filters_in(filters)))

    @classmethod
    def _and_not_in_query(cls, filters):
        """Execute AND NOT IN query.

        Returns BaseQuery.
        """
        return cls.query.filter(db.and_(*cls._filters_not_in(filters)))

    @classmethod
    def _or_query(cls, filters):
        """Execute OR query.

        Returns BaseQuery.
        """
        return cls.query.filter(db.or_(*cls._filters(filters)))

    @classmethod
    def _or_in_query(cls, filters):
        """Execute OR IN query.

        Returns BaseQuery.
        """
        return cls.query.filter(db.or_(*cls._filters_in(filters)))

    @classmethod
    def _or_not_in_query(cls, filters):
        """Execute OR NOT IN query.

        Returns BaseQuery.
        """
        return cls.query.filter(db.or_(*cls._filters_not_in(filters)))