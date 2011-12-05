# -*- coding: UTF-8 -*-
#
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Various utilities used in the controllers


import os.path
import traceback

from turbogears import config

from controllers import convert, page

_testing = False

def send_email(template, recipients=[], cc=[], bcc=[], params={}):
    import turbomail

    def replace(field, params):
        for key, value in params.iteritems():
            field = field.replace(u'${%s}' % key, unicode(value))
        return field

    template = os.path.join(config.get('mail.templates', ''), template + '.txt')
    if not os.path.exists(template):
        raise ValueError('Template %s does not exist' % template)

    file = open(template, 'r')
    subject = replace(unicode(file.readline().strip(), 'UTF-8'), params)
    content = replace(unicode(file.read(), 'UTF-8'), params)
    file.close()

    sender = list(config.get('mail.sender'))
    if isinstance(recipients, (str, unicode)):
        recipients = [recipients]
    elif not isinstance(recipients, list):
        recipients = list(recipients)
    if not isinstance(cc, list):
        cc = list(cc)
    if not isinstance(bcc, list):
        bcc = list(bcc)
    
    message = turbomail.Message(subject=subject, sender=sender,
        recipient=recipients, cc=cc, bcc=bcc)
    message.plain = content

    turbomail.enqueue(message)

def split_list(argument_list, sep, remove_empty=True):
    """Split the strings in the list using the separator sep.
    
	>>> split_list(['a.b', 'c.d'], '.')
	['a', 'b', 'c', 'd']

    """

    result_list = []
    for l in argument_list:
	result_list.extend(l.split(sep))
    if remove_empty:
	result_list = filter(lambda l: l, result_list)
    return result_list

def in_tuples(iterable, size=2):
    """Returns the iterable items in tuples.

        >>> list(in_tuples([1, 2, 3, 4, 5, 6]))
        [(1, 2), (3, 4), (5, 6)]

    Takes the size parameter

        >>> list(in_tuples(['a', 'b', 'd', 'c', 'fg', 'rr'], size=3))
        [('a', 'b', 'd'), ('c', 'fg', 'rr')]

        >>> list(in_tuples([1, 2, 3, 4, 5, 6], size=1))
        [(1,), (2,), (3,), (4,), (5,), (6,)]

    If the iterable length can not be divided to integer, returns Nones at the
    end

        >>> list(in_tuples([1, 3, 5, 7], size=3))
        [(1, 3, 5), (7, None, None)]

    Empty list transforms into an empty list

        >>> list(in_tuples([]))
        []
    """
    tup = []
    s = 0
    for i in iterable:
        tup.append(i)
        s += 1
        if s == size:
            yield tuple(tup)
            tup = []
            s = 0
    if tup:
        for t in range(size - len(tup)):
            tup.append(None)
        yield tuple(tup)


def callservice(url, method='post', basicauth=None, **kargs):
    from urllib import urlencode
    from urllib2 import (urlopen, build_opener, install_opener, HTTPError,
        HTTPBasicAuthHandler)
    params = ''
    if kargs:
        # urlencode does not accept non-ascii data
        for k, v in kargs.iteritems():
            if isinstance(v, unicode):
                kargs[k] = v.encode('utf-8')
        params = urlencode(kargs)
    if not _testing:
        # If we need to authenticate
        if basicauth is not None:
            # Get host from url
            host = url[url.find('//') + 2:]
            for c in (':', '/', '?', '&'):
                if c in host:
                    host = host[:host.find(c)]
            # Install authentication handler
            auth_handler = HTTPBasicAuthHandler()
            auth_handler.add_password(basicauth['realm'], host,
                basicauth['user'], basicauth['passwd'])
            install_opener(build_opener(auth_handler))
        try:
            if method == 'post':
                u = urlopen(url, data=params)
            elif method == 'get':
                if params:
                    url = '%s?%s' % (url, params)
                u = urlopen(url)
            else:
                raise ValueError('Unknown method: %s' % method)
        except HTTPError, e:
            raise ValueError(e.read())
        resp = u.read()
        return resp
    else:
        if params:
            url = '%s?%s' % (url, params)
        from idileslib.turbogears.testing import Browser
        browser = Browser()
        browser.goto(url)
        return browser.body

def _unjsonify(text):
    import jsonlib
    return jsonlib.read(text)

class Service(object):
    def __init__(self, url, method='post', auth=None, *args, **kargs):
        """Constructs a proxy object for a remote service.

    url - A URL of the service
    method - HTTP method: get or post. Default post
    auth - dict(realm=<realm>, user=<username>, passwd=<password>). Default None
        """
        super(Service, self).__init__(*args, **kargs)

        from urllib2 import HTTPError

        # Add the missing parts of address to the url
        url = url.lower()
        if url.startswith('/'):
            url = 'http://%s:%s%s' % (config.get('server.hostname'),
                config.get('server.socket_port'), url)
        elif not url.startswith('http://'):
            url = 'http://%s' % url

        try:
            res = _unjsonify(callservice(url, method=method, basicauth=auth))
        except HTTPError:
            raise ValueError('Service not found at %s' % url)
        self.url = url
        self.method = method
        self.auth = auth

        for method in res[u'methods']:
            setattr(self, method, self.__hide(method))


    def __hide(self, name):
        from urllib2 import HTTPError

        def method(**kargs):
            url = '/'.join((self.url, name))
            try:
                res = _unjsonify(callservice(url, method=self.method,
                    basicauth=self.auth, **kargs))
            except HTTPError, e:
                raise AttributeError('Invalid arguments: %s' % e.message)
            return res

        if isinstance(name, unicode):
            name = name.encode('UTF-8')
        method.__name__ = name
        return method


def put_watermark(photo, logo, blend=0.2):
    """Puts logo into the photo as a watermark.
    """
    import Image

    photo = photo.convert('RGBA')
    photo.format = 'PNG'

    logo = logo.convert('RGBA')
    logo.thumbnail(photo.size, Image.ANTIALIAS)

    width, height = ((photo.size[0] - logo.size[0]) / 2,
        (photo.size[1] - logo.size[1]) / 2)

    # Create a logo same size as the photo
    sized_logo = Image.new('RGBA', photo.size)
    sized_logo.paste(logo, (width, height), logo)

    # Make the blended image
    blended = Image.blend(photo, sized_logo, blend)
    
    # Paste the blended part onto the original
    photo.paste(blended, (0, 0), sized_logo)
    return photo
