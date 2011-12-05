# -*- coding: UTF-8 -*-
#
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Validators

from formencode.validators import FieldsMatch, Invalid

# Fix the FieldsMatch validator
def validate_python(self, field_dict, state):
    errors = {}
    try:
        self._blind_validate_python(field_dict, state)
    except KeyError:
        for name in self.field_names:
            if not name in field_dict:
                errors[name] = 'Field value missing'
        raise Invalid('', field_dict, state, error_dict=errors)

FieldsMatch._blind_validate_python = FieldsMatch.validate_python
FieldsMatch.validate_python = validate_python
