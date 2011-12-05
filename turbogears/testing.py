# -*- coding: UTF-8 -*-
#
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#

import urllib
import cherrypy
from Cookie import SimpleCookie
from turbogears import config, testutil
from turbogears.testutil import createRequest
from turbogears.i18n.tg_gettext import plain_gettext

__builtins__['ugettext'] = plain_gettext

def cookie_header(morsel):
    """Returns a dict containing cookie information to pass to a server."""
    return {'Cookie': morsel.output(header="")[1:]}

class Browser(object):
    def __init__(self, Visit=None):
        if Visit is not None:
            Visit.createTable(ifNotExists=True)
            self.visit = True
        else:
            self.visit = False
        self.cookie = SimpleCookie()

    def goto(self, url, **kargs):
        params = kargs.get('params')
        if params:
            s = '&'.join(['='.join([urllib.quote_plus(str(k)),
                urllib.quote_plus(str(v))]) for k, v in params.items()])
            url += '?' + s
            del kargs['params']
        if self.cookie:
            headers = kargs.get('headers', {})
            headers['Cookie'] = self.cookie.output()
            kargs['headers'] = headers
        createRequest(url, **kargs)
        if cherrypy.response.simple_cookie:
            self.cookie.update(cherrypy.response.simple_cookie)

        # Try to handle redirects
        i = 5   # To prevent infinitive redirects
        while cherrypy.response.status.startswith('302') and i > 0:
            response = cherrypy.response.body[0]
            url = response.split('>')[1].split('<')[0]
            if self.cookie:
                headers = kargs.get('headers', {})
                headers['Cookie'] = self.cookie.output()
                kargs['headers'] = headers
            createRequest(url, **kargs)
            if cherrypy.response.simple_cookie:
                self.cookie.update(cherrypy.response.simple_cookie)
            i -= 1

        self.url = url
        self.response = cherrypy.response
        try:
            self.body = cherrypy.response.body[0]
        except:
            self.body = None
        if not self.response.status.startswith('200'):
            raise ValueError(self.body)

    def response_contains(self, text):
        return text in self.body
