# -*- coding: UTF-8 -*-
#
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Forms

from datetime import datetime
from random import choice
from string import letters
from tw import forms


class JSListForm(forms.Form):
    template = 'forms.templates.forms.jslistform'

    params = list(forms.Form.params) + ['submit', 'cancel_text',
        'cancel_link',
        'cancel_action',
        'show_labels', 'ajax', 'field_dict', 'on_success']
    show_labels = True
    ajax = True
    on_success = 'function() {}'

    def __init__(self, id=None, parent=None, children=[], **kargs):
        super(JSListForm, self).__init__(id, parent, children, **kargs)
        if self.id:
            forms.HiddenField('form_id__', self, default=self.id)
        self.field_dict = dict([(f.id_path_elem, f) for f in self.children])


class JSLineForm(forms.Form):
    template = 'forms.templates.forms.jslineform'

    params = list(forms.Form.params) + ['submit', 'cancel_text',
        'cancel_link',
        'cancel_action',
        'show_labels', 'ajax', 'field_dict', 'on_success']
    show_labels = True
    ajax = True
    on_success = 'function() {}'

    def __init__(self, id=None, parent=None, children=[], **kargs):
        super(JSLineForm, self).__init__(id, parent, children, **kargs)
        if self.id:
            forms.HiddenField('form_id__', self, default=self.id)
        self.field_dict = dict([(f.id_path_elem, f) for f in self.children])

