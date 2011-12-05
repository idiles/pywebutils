# -*- coding: UTF-8 -*-
#
# Kiveda.lt
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Various utilities for controllers

from turbogears.util import request_available

def get_select_options(cls, id='id', title='title', with_none=True,
    filter=None, order=None):
    if not order:
        order = title
    def select():
        if request_available():
            result = cls.select().orderBy(order)
            if filter:
                result = result.filter(filter)
            options = [(getattr(o, id), getattr(o, title)) for o in result]
            if with_none or not options:
                options.insert(0, ('', u''))
        else:
            options = [('', u'')]
        return options
    return select
