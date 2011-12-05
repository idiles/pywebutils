# -*- coding: UTF-8 -*-
#
# Idiles.lt
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Forms.

import os

from sqlobject import SQLObjectNotFound
from sqlobject.sqlbuilder import AND
from turbogears import validators
# import logging
# log = logging.getLogger("kivedaweb.controllers")


class Exists(validators.FancyValidator):
    """Checks if there is an object in the DB with the same attribute value."""

    errors = {'exists': _(u'Toks %s neegzistuoja')}

    def _to_python(self, value, state):
        if not hasattr(self, 'attr_name'):
            self.attr_name = 'id'
        if not hasattr(self, 'attr_title'):
            self.attr_title = 'ID'
        if isinstance(value, unicode):
            value = value.encode('UTF-8')
        params = {self.attr_name: value}
        if self.cls.selectBy(**params).count() == 0:
            raise validators.Invalid(self.errors['exists'] % \
                self.attr_title, value, state)
        return value


class Unique(validators.FancyValidator):
    """Checks if the attribute value would be unique in the DB.
    
    If the id is provided then the object having that id would not be checked.
    
    """

    errors = {'exists': _(u'Toks %s jau egzistuoja')}

    def _to_python(self, fields, state):
        if not hasattr(self, 'db_name'):
            self.db_name = self.attr_name
        params = {self.db_name: fields[self.attr_name]}
        objs = self.cls.selectBy(**params)
        if 'id' in fields:
            id = fields['id']
            objs = objs.filter(self.cls.q.id != id)
        if objs.count() > 0:
            raise validators.Invalid(u'', fields, state,
                error_dict={self.attr_name: self.errors['exists'] % self.attr_title})
        return fields


class ConvertToObject(validators.FancyValidator):
    """Returns an object based on class and id
    
    If the id is 0 then return None
    
    """

    def _to_python(self, value, state):
        if hasattr(self, 'allow_none'):
            if self.allow_none and int(value) == 0:
                return None
        try:
            return self.cls.get(int(value))
        except SQLObjectNotFound:
            raise validators.Invalid(_(u'Toks objektas neegzistuoja'),
                value, state)

class LengthOneOf(validators.FancyValidator):
    """Checks if the length of the input string is in set.

        >>> val = LengthOneOf(length=range(1, 5))
        >>> val.to_python('abcd')
        'abcd'
        >>> val.to_python('abcde')
        Traceback (most recent call last):
        ...
        Invalid: Neteisingas ilgis
    """

    def _(s): return s

    gettextargs = {}

    messages = {
        'badLength': _(u"Neteisingas ilgis")
    }

    def __init__(self, length=[], *args, **kargs):
        super(LengthOneOf, self).__init__(*args, **kargs)
        self.length = length

    def _to_python(self, value, state):
        if len(value) not in self.length:
            raise validators.Invalid(self.message('badLength', state),
                value, state)
        return value

