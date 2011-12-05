# -*- coding: UTF-8 -*-
#
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Pylons ajax helpers

from random import choice
from genshi import Markup
from pylons import request

def jsviewlet(url):
    id = 'js' + ''.join([choice(letters) for i in range(18)])
    js = '''var callback = {success: function(o)
    {set_and_eval(document.getElementById('%s'), o.responseText);}};
    YAHOO.util.Connect.asyncRequest('GET', '%s', callback)''' % (id, url)
    return Markup('<script type="text/javascript">%s</script>'
        '<span id="%s"></span>' % (js, id))

def viewlet(url):
    try:
        include = request.environ['paste.recursive.include']
        resp = Markup(unicode(include(url).body, 'utf-8'))
        del request.environ['paste.recursive.previous_environ']
        request.environ['paste.recursive.include'] = include
        return resp
    except ForwardRequestException:
        return jsviewlet(url)

def jsredirect(url, uploaded=False):
    """Redirect page using Javascript call. This function is useful for AJAX
    forms. Just return jsredirect(...) output to your form and it will
    reload the page.

    Set 'uploaded' to True if your AJAX form has file fields.
    """
    parent = ''
    if uploaded:
        parent = '.parent'
    return '''
    <script type="text/javascript">
        window%s.location = '%s';
    </script>''' % (parent, url)

def jsreload():
    return '''
    <script type="text/javascript">
        window.location.reload(true);
    </script>'''

def reload_container(container_id, url, params={}):
    """Get content using AJAX call from 'url' and put it to an element with
    ID 'container_id'.
    """
    return """
        <script type="text/javascript">
            $('#%s').html('<img src="/images/spinner.gif" alt="" />');
            $('#%s').load('%s', %s);
        </script>
    """ % (container_id, container_id,  url, repr(params))

def show_message(container_id, message):
    """Put message text into an element with ID 'container_id'.
    """
    return """
        <script type="text/javascript">
            $('#%s').html('%s').show();
        </script>
    """ % (container_id, message)

