# -*- coding: UTF-8 -*-
#
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Forms

from decorator import decorator
from pylons import request
from tw.mods.pylonshf import valid

from forms import *
from validators import *
from widgets import *

def validate(form, on_success, post_only=False):
    def entangle(func):
        def _validator(func, cont, *args, **kargs):
            params = dict(post_only and request.POST or request.params)
            if params.get('form_id__') == form.id:
                if valid(func, form=form, post_only=post_only):
                    result = func.form_result
                    del result['form_id__']
                    resp = on_success(cont, **result)
                    if args and args[-1] is None:
                        args = list(args[:-1]) + [resp]
            return func(cont, *args, **kargs)
        return decorator(_validator)(func)
    return entangle
