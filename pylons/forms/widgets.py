# -*- coding: UTF-8 -*-
#
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Widgets

from datetime import datetime
from random import choice
from string import letters
from tw import forms


class FieldList(forms.FieldSet):
    template = "forms.templates.fieldlist"


class CalendarButton(forms.FormField):
    template = 'forms.templates.calendarbutton'

    params = list(forms.FormField.params) + ['date_format', 'not_empty',
        'min_date', 'max_date']

    date_format = "%Y-%m-%d"
    validator = None
    not_empty = True

    def __init__(self, *args, **kargs):
        super(CalendarButton, self).__init__(*args, **kargs)
        if not self.validator:
            self.validator = forms.validators.DateTimeConverter(
                format=self.date_format, not_empty=self.not_empty)

        if not 'default' in kargs:
            self.default = lambda: datetime.now().date()

    def update_params(self, d):
        super(CalendarButton, self).update_params(d)
        d['random_id'] = 'cal' + ''.join([choice(letters) for i in range(12)])
        if d['value']:
            value_d = d['value']
            if callable(value_d):
                value_d = value_d()
            d['cal_value'] = value_d.strftime('%m/%d/%Y')
            d['value'] = value_d.strftime(self.date_format)
        else:
            d['cal_value'] = ''

        if d.get('min_date'):
            min_date = d['min_date']
            if callable(min_date):
                min_date = min_date()
            d['cal_min_date'] = min_date.strftime('%m/%d/%Y')
        else:
            d['cal_min_date'] = ''
        
        if d.get('max_date'):
            max_date = d['max_date']
            if callable(max_date):
                max_date = max_date()
            d['cal_max_date'] = max_date.strftime('%m/%d/%Y')
        else:
            d['cal_max_date'] = ''


class YUICalendar(forms.FormField):
    template = 'forms.templates.yuicalendarfield'

    params = list(forms.FormField.params) + ['date_format', 'not_empty']

    date_format = "%Y-%m-%d"
    validator = None
    not_empty = True

    def __init__(self, *args, **kargs):
        super(YUICalendar, self).__init__(*args, **kargs)
        if not self.validator:
            self.validator = forms.validators.DateTimeConverter(
                format=self.date_format, not_empty=self.not_empty)

        if not self.default:
            self.default = lambda: datetime.now().date()

    def update_params(self, d):
        super(YUICalendar, self).update_params(d)
        d['random_id'] = 'cal' + ''.join([choice(letters) for i in range(12)])
        d['cal_value'] = d['value'].strftime('%m/%d/%Y')


class YUIEditor(forms.FormField):
    template = 'forms.templates.yuieditorfield'
    
    params = list(forms.FormField.params) + ['width', 'height']

    width = '500px'
    height = '300px'

    def update_params(self, d):
        super(YUIEditor, self).update_params(d)
        d['random_id'] = 'edt' + ''.join([choice(letters) for i in range(12)])

class Separator(forms.FormField):
    template = "forms.templates.separator"
    suppress_label = True

    
