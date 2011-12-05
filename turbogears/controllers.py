# -*- coding: UTF-8 -*-
#
# Kiveda.lt
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Various utilities for controllers

from turbogears import (flash, redirect, view, validate as tg_validate,
    error_handler)
from cherrypy import session

from utils import _to_lower_case


class TemplateVariables(object):
    """Class that provides variables for the templates
    
    If your templates need additional variables you should subclass your
    variable class from this class. The name of the class should end with
    'Variables'

        >>> class TestVariables(TemplateVariables):
        ...     some_var = 3

    We need to register this class to make its variables accessible

        >>> TestVariables.register()

    Now we should be able to access the variables from our views under the name
    'test'

        >>> from turbogears import view
        >>> vars = {}
        >>> returns = [foo(vars) for foo in view.variable_providers]
        >>> 'test' in vars
        True
    
    And we can get 'some_var' from the provider
        
        >>> vars['test'].some_var
        3
    """

    def __add_template_vars(self, vars):
        """Register the variable_class as the variable provider"""
        return vars.update({self.class_name: self})

    @classmethod
    def register(cls):
        name = cls.__name__.rsplit('Variables')[0]
        cls.class_name = _to_lower_case(name)

        variable_object = cls()
        view.variable_providers.append(variable_object.__add_template_vars)


def convert(params=[], on_error=''):
    """Convert input args to objects using the object supplied

    @param params: list of tuples of function params to be converted:
        (parameter_name, convert_to_object [, fallback value if not found])
    @param on_error: url to redirect on error

    """

    def entangle(foo):
        def converter(self, *args, **kargs):
            def find_param(name):
                if name in kargs:
                    return kargs[name]
                if args:
                    return args.pop(0)
                if name in session:
                    return session[name]

            def conv(obj, param):
                if hasattr(obj, 'selectBy'):
                    return obj.get(int(param))
                else:
                    return obj(param)

            args = list(args)
            ckargs = {}
            for cp in params:
                name = cp[0]
                obj = cp[1]
                if len(cp) == 2:    # Required argument
                    try:
                        param = find_param(name)
                        assert param is not None
                        ckargs[name] = conv(obj, param)
                    except:
                        flash(_(u'Neteisingi arba nepilni parametrai'))
                        raise redirect(on_error)
                    session[name] = param
                else:               # Optional argument
                    alt = cp[2]
                    param = kargs.get(name, None)
                    try:
                        ckargs[name] = conv(obj, param)
                    except:
                        ckargs[name] = alt

            return foo(self, **ckargs)
        conv = converter
        conv.__module__ = foo.__module__
        return conv
    return entangle

def page(foo):
    foo.public_link = True
    return foo

def validate(action, form=None, validators=None, flash=None):
    def entangle(foo):
        def validator(self, *args, **kargs):
            @error_handler()
            @tg_validate(form=form, validators=validators)
            def get_errors(self, *args, **kargs):
                tg_errors = kargs.pop('tg_errors', None)
                return tg_errors, args, kargs

            action_result = None
            errors = None

            # If the validated function has arguments itself, we have to strip
            # them
            c = foo.func_code
            default_args = {}
            for i in range(c.co_argcount):
                arg_name = c.co_varnames[i]
                if arg_name in kargs and arg_name != 'self':
                    default_args[arg_name] = kargs[arg_name]
                    del kargs[arg_name]
            if kargs:
                errors, args, kargs = get_errors(self, *args, **kargs)
                if not errors:
                    action_result = action(self, **kargs)

            # Put back the function arguments
            kargs.update(default_args)
            kargs['action_result'] = action_result
            kargs['errors'] = errors
            return foo(self, *args, **kargs)
        val = validator
        val.__module__ = foo.__module__
        return val
    return entangle


def handle(form, handler):
    try:
        __form_id = filter(lambda f: f.name == 'formid',
            form.fields)[0].default
    except IndexError:
        raise KeyError('Form used with handle must have a formid')

    def entangle(foo):
        def validator(self, *args, **kargs):
            if __form_id != kargs.get('formid', ''):
                # Do not do anything
                return foo(self, *args, **kargs)

            formid = kargs.pop('formid')

            handler_result = None
            errors = None

            @error_handler()
            @tg_validate(form=form)
            def get_errors(self, *args, **kargs):
                tg_errors = kargs.pop('tg_errors', None)
                return tg_errors, args, kargs

            if kargs:
                errors, args, kargs = get_errors(self, *args, **kargs)
                if not errors:
                    handler_result = handler(self, *args, **kargs)

            # Put back the function arguments
            kargs['handler_result'] = dict(result=handler_result, errors=errors)
            return foo(self, *args, **kargs)
        val = validator
        val.__module__ = foo.__module__
        return val
    return entangle

def decoding_filter_patch():
    import cherrypy
    def decode(self, enc):
        decodedParams = {}
        for key, value in cherrypy.request.params.items():
            if hasattr(value, 'file'):
                # This is a file being uploaded: skip it
                decodedParams[key] = value
            elif isinstance(value, list):
                # value is a list: decode each element
                decodedParams[key] = [v.decode(enc) for v in value]
            else:
                # Sometimes the value is already unicode and we do not need to
                # decode it. LJ.
                if isinstance(value, str):
                    # value is a regular string: decode it
                    decodedParams[key] = value.decode(enc)
                else:
                    decodedParams[key] = value
        
        # Decode all or nothing, so we can try again on error.
        cherrypy.request.params = decodedParams
        
    from cherrypy.filters.decodingfilter import DecodingFilter
    DecodingFilter.decode = decode
