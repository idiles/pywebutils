# -*- coding: UTF-8 -*-
#
# Copyright (c) 2008 IDILES SYSTEMS, UAB
#
# Authentication and authorization helpers

from decorator import decorator
from paste.request import parse_formvars
from pylons import request

def require(perm):
    """Makes the provided function require some permissions.
    """
    def entangle(func):
        def caller(func, *args, **kargs):
            perm()
            # Remove login credentials
            form = parse_formvars(request.environ, include_get_vars=True)
            if form.pop('do_login__', None):
                form.pop('login', None)
                form.pop('password', None)
            return func(*args, **kargs)
        try:
            # Old Decorators version
            return decorator(caller)(func)
        except:
            # New version
            return decorator(caller, func)
    return entangle

