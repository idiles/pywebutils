#
# IDILES Library
# Copyright (c) 2007 IDILES SYSTEMS Ltd
#

class DataObject(dict):
    """Simple object class to store data.
    
    How to use it:
        >>> obj = DataObject(name='John', email='john@idiles.com')
        >>> obj.name
        'John'
        >>> obj.age = 25
        >>> obj.age
        25
        >>> obj['age']
        25
        >>> print obj
        <DataObject: age=25, email='john@idiles.com', name='John'>
    """

    def __init__(self, **kargs):
        dict.__init__(self, kargs)

    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if self.__dict__.has_key(key):
            dict.__setattr__(self, key, value)
        else:
            self.__setitem__(key, value)

    def __str__(self):
        sorted = [(key, value) for key, value in self.items()]
        sorted.sort()
        return '<DataObject: %s>' \
            % ', '.join(['='.join([k, repr(v)]) for k, v in sorted])

