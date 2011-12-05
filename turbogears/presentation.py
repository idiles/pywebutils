# -*- coding: UTF-8 -*-
#
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Various utilities for presentation

import re

def blurb(text, length=30):
    """Return the beginning of text.

    If the text is short do not change it

        >>> blurb('This is a short text', length=30)
        'This is a short text'

    If it is long, truncate it and put ellipsis at the end

        >>> blurb('This is a very very very very very long text', length=22)
        'This is a very very...'
    """

    if len(text) > length:
        text = text[:length - 3] + '...'
    else:
        text = text[:length]
    return text

def render_html(text):
    r"""Transform text into HTML-ready text with some markup.

    Paragraphs are converted properly.

        >>> text = 'One\nTwo\r\nThree\rFour'
        >>> render_html(text)
        'One<br />Two<br />Three<br />Four'

    Bold text is recognized.

        >>> text = 'This is *wonderful*!'
        >>> render_html(text)
        'This is <strong>wonderful</strong>!'

    Hyperlinks are processed.

        >>> text = 'Please visit http://www.idiles.lt and ' + \
        ...     'http://m.idiles.lt/?id=11;&name.'
        >>> html = 'Please visit <a href="http://www.idiles.lt" target="_blank">http://www.idiles.lt</a> ' \
        ...     'and <a href="http://m.idiles.lt/?id=11;&name" target="_blank">http://m.idiles.lt/?id=11;&name</a>.'
        >>> html == render_html(text)
        True

    You can combine hyperlinks with paragraphs.

        >>> text = 'Visit:\n- http://www.idiles.lt\n' + \
        ...     '- http://m.idiles.lt\nand http://www.idiles.com\n'
        >>> html = render_html(text)
        >>> '\n' in html
        False
        >>> print '\n'.join(html.split('<br />'))
        Visit:
        - <a href="http://www.idiles.lt" target="_blank">http://www.idiles.lt</a>
        - <a href="http://m.idiles.lt" target="_blank">http://m.idiles.lt</a>
        and <a href="http://www.idiles.com" target="_blank">http://www.idiles.com</a>

    The same hyperlink appearing several times is handled correctly

        >>> text = 'http://www.idiles.lt/#,\n<a href=" http://www.idiles.lt " >'
        >>> print '\n'.join(render_html(text).split('<br />'))
        <a href="http://www.idiles.lt/#" target="_blank">http://www.idiles.lt/#</a>,
        &lt;a href=" <a href="http://www.idiles.lt" target="_blank">http://www.idiles.lt</a> " &gt;

    Unicode text is not a problem.

        >>> text = u'\xc5\xbealia giria'
        >>> result = render_html(text)

    """

    text = text.replace('<', '&lt;').replace('>', '&gt;')

    # Then replace hyperlinks
    url_first = r'[A-Za-z0-9]'
    url_chars = r'[-A-Za-z0-9/#&@$.:;%?=_+\\]'
    url_last = r'[A-Za-z0-9/#&$%=]'

    text = re.sub(r'http://(%s%s*%s)' % (url_first, url_chars, url_last),
        r'<a href="http://\1" target="_blank">http://\1</a>', text)

    # Find all *BOLDTEXT* patterns.
    bold = re.compile(r'\*.*\*')
    items = set(bold.findall(text))
    for item in items:
        block = item[1:-1]
        text = text.replace(item, '<strong>%s</strong>' % block)

    # Split paragraphs
    text = '<br />'.join(text.splitlines())

    return text

def fix_paginate_url(url, params):
    """Fix the url created by the paginate.

    A call without params is a noop

        >>> fix_paginate_url('/test/this?op1=2&3=5', params=[])
        '/test/this?op1=2&3=5'

    If we provide a parameter it is removed

        >>> fix_paginate_url('/test/12?removeme=12',
        ...     params=['removeme'])
        '/test/12'

        >>> fix_paginate_url('/test/12?param=3&removeme=12&other=1',
        ...     params=['removeme'])
        '/test/12?param=3&other=1'

    It is not removed if it is not found

        >>> fix_paginate_url('/test/12?param=3&removeme=12&other=1',
        ...     params=['remove'])
        '/test/12?param=3&removeme=12&other=1'

    Case is not important

        >>> fix_paginate_url('/test/12?param=3&rEmOvEmE=12&other=1',
        ...     params=['ReMoVeMe'])
        '/test/12?param=3&other=1'

    And we accept some corner case arguments

        >>> fix_paginate_url('/test/12?parambad=&removeme=12&=strange&thing',
        ...     params=['removeme'])
        '/test/12?parambad=&=strange&thing'

        >>> fix_paginate_url('/test/12', params=['removeme'])
        '/test/12'

        >>> fix_paginate_url('?param=1&removeme=12&=strange&thing',
        ...     params=['removeme'])
        '?param=1&=strange&thing'

    """
    def partition(arg, s):
        pos = arg.find(s)
        if pos == -1:
            return (arg, '', '')
        else:
            return (arg[:pos], s, arg[pos + len(s):])

    if '?' in url:
        contr, sep, pars = partition(url, '?')
    else:
        return url
    url = contr
    if '//' in contr:
        pref, s, contr = partition(contr, '//')
    contr = contr.split('/')
    pars = pars.split('&')
    params = [p.lower() for p in params]
    for p in pars:
        if '=' in p:
            name, s, value = partition(p, '=')
            if name.lower() in params:
                continue
        url = sep.join((url, p))
        sep = '&'
    return url
