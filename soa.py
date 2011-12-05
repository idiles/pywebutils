# -*- coding: UTF-8 -*-
#
# Copyright (c) 2008 IDILES SYSTEMS, UAB
#

import os.path
import traceback
from simplejson import loads, dumps
from urllib import urlencode
from urllib2 import Request, urlopen, HTTPError

from idileslib.data import DataObject

_testing = False

dragonfly_esb_locations = {}

def webmethod(func, type='json'):
    func.func_dict['webmethodtype'] = type
    return func


def callservice(url__, **kargs):
    kw = {}
    if kargs:
        # urlencode does not accept non-ascii data
        for k, v in kargs.iteritems():
            if isinstance(v, unicode):
                kargs[k] = v.encode('utf-8')
        kw['data'] = urlencode(kargs)
    if not _testing:
        req = Request(url__, **kw)
        u = urlopen(req)
        return u.read()
    else:
        kargs = '&'.join(['='.join((k, str(v)))
            for k, v in kargs.iteritems()])
        if kargs:
            url__ = '%s?%s' % (url__, kargs)
        from idileslib.turbogears.testing import Browser
        browser = Browser()
        browser.goto(url__)
        return browser.body


def _jsonify(data):
    return loads(data)


class ServiceProxy(object):
    def __init__(self, name__, *args, **kargs):
        super(ServiceProxy, self).__init__(*args, **kargs)
        locations = ServiceProxy.get_locations(name=name__)
        if len(locations) == 0:
            raise ValueError('No locations defined for serivice %s' % \
                name__)
        url = locations[0]

        try:
            res = _jsonify(callservice(url))
        except HTTPError:
            raise ValueError('Service not found at %s' % url)

        for method in res[u'methods']:
            setattr(self, method, self.__hide(method))

        self.url = url

    def __hide(self, name):
        def method(**kargs):
            url = '/'.join((self.url, name))
            try:
                res = _jsonify(callservice(url, **kargs))
                try:
                    if 'valueerror_' in res:
                        err = res['valueerror_']
                        del res['valueerror_']
                        raise ValueError(err)
                except TypeError:
                    pass

                return res
            except HTTPError, e:
                raise RuntimeError('Error: %s' % e)

        if isinstance(name, unicode):
            name = name.encode('UTF-8')
        method.__name__ = name
        return method

    @staticmethod
    def add_location(name, location):
        """Adds web service location (URL) to the global Dragonfly ESB
        location registry.
        """
        global dragonfly_esb_locations
        locations = dragonfly_esb_locations.get(name, [])
        if not location in locations:
            locations.append(location)
        dragonfly_esb_locations[name] = locations

    @staticmethod
    def remove_location(name, location):
        """Removes web service location (URL) from the global Dragonfly ESB
        location registry.
        """
        global dragonfly_esb_locations
        locations = dragonfly_esb_locations.get(name, [])
        if location in locations:
            locations.remove(location)
        dragonfly_esb_locations[name] = locations

    @staticmethod
    def load_locations(path):
        """Load web service locations from Dragonfly ESB location
        configuration file.
        """
        global dragonfly_esb_locations

        for line in open(path).readlines():
            line = line.strip()
            if line.startswith('#'):
                continue
        
            if '=' in line:
                name, location = line.split('=')
                name = name.strip()
                location = location.strip()
                ServiceProxy.add_location(name, location)
            
    @staticmethod
    def get_locations(name=None):
        """Get web service locations from Dragonfly ESB location
        registry.
        """
        global dragonfly_esb_locations
        if name:
            try:
                return dragonfly_esb_locations[name]
            except KeyError:
                raise ValueError('Uknown location for web service: %s' % name)
        else:
            return dragonfly_esb_locations

