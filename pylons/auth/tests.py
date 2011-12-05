# -*- coding: UTF-8 -*-
#
# Copyright (c) 2008 IDILES SYSTEMS, UAB
#
# Authentication and authorization helper tests

def test_require():
    r"""Test the 'require' function.
    
        >>> from auth import require
    
    This function takes one argument - a condition:
        
        >>> logged_in = True
        >>> def cond():
        ...     def check_logged():
        ...         if not logged_in:
        ...             raise ValueError('Not logged in')
        ...     return check_logged

    And decorates another function

        >>> @require(cond())
        ... def index():
        ...     return '<html></html>'

    As the user has logged in we should get the normal output

        >>> index()
        '<html></html>'

    Now log the user out and try again

        >>> logged_in = False
        >>> index()
        Traceback (most recent call last):
            ...
        ValueError: Not logged in

    Try require with the function that needs arguments

        >>> @require(cond())
        ... def sum(a, b):
        ...     return a + b

        >>> sum(3, 4)
        Traceback (most recent call last):
            ...
        ValueError: Not logged in

        >>> logged_in = True
        >>> sum(3, b=4)
        7

    """

