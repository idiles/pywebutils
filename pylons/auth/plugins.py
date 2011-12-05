# -*- coding: UTF-8 -*-
#
# Copyright (c) 2008 IDILES SYSTEMS, UAB
#
# Authentication and authorization plugins for repoze.who

from paste.recursive import ForwardRequestException
from paste.request import parse_formvars
from repoze.who.interfaces import IChallengeDecider
from repoze.who.plugins.form import FormPlugin
from repoze.who.plugins.auth_tkt import _bool, AuthTktCookiePlugin
import zope.interface


class PostFormPlugin(FormPlugin):
    def identify(self, environ):
        form = parse_formvars(environ, include_get_vars=False)
        if form.get(self.login_form_qs, None):
            try:
                login = form['login']
                password = form['password']
            except KeyError:
                return None
            return dict(login=login, password=password)
        
def make_form_plugin(login_form_qs='do_login__', rememberer_name=None,
    login_path='/login'):
    if rememberer_name is None:
        raise ValueError(
            'must include rememberer key (name of another IIdentifier plugin)')
    # If unauthenticated forward to login page
    def formcallable(environ):
        raise ForwardRequestException(login_path)
    plugin = PostFormPlugin(login_form_qs,
        rememberer_name, formcallable=formcallable)
    return plugin


class CustomAuthTktCookiePlugin(AuthTktCookiePlugin):
    def remember(self, environ, identity):
        if environ.get('repoze.who.identity'):
            return AuthTktCookiePlugin.remember(self, environ, identity)
        else:
            return self.forget(environ, identity)

def make_authtkt_plugin(secret=None, cookie_name='auth_tkt', secure=False,
    include_ip=False):
    if secret is None:
        raise ValueError('secret must be None')
    plugin = CustomAuthTktCookiePlugin(secret, cookie_name, _bool(secure),
        _bool(include_ip))
    return plugin

def challenge_401_403(environ, status, headers):
    return status.startswith('401 ') or status.startswith('403 ')
zope.interface.directlyProvides(challenge_401_403, IChallengeDecider)
