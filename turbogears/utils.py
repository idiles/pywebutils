# -*- coding: UTF-8 -*-
#
# Kiveda.lt
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Various utilities


def _to_lower_case(name, sep='_'):
    """Return the name converted to lowercase and dashed.

        >>> _to_lower_case('Thing')
        'thing'
        >>> _to_lower_case('CamelCase')
        'camel_case'
        >>> _to_lower_case('XMLRpcConnection')
        'xml_rpc_connection'
        >>> _to_lower_case('ALLCAPITALS')
        'allcapitals'
        >>> _to_lower_case('ALL_CAPITALS')
        'all_capitals'
        >>> _to_lower_case('lower_case_string')
        'lower_case_string'
        >>> _to_lower_case('This_is_Very_BAD_Style')
        'this_is_very_bad_style'
        >>> _to_lower_case('Certificate')
        'certificate'
    """
    all_parts = []
    splitted_name = name.split(sep)
    for name in splitted_name:
        part = ''
        parts = []
        for s in name:
            if s.isalpha() and s.isupper():
                s = s.lower()
                if part != '':
                    parts.append(part)
                part = s
            else:
                part += s
        parts.append(part)

        i = 1
        while i < len(parts):
            if len(parts[i]) == 1:
                parts[i-1] += parts[i]
                del parts[i]
            else:
                i += 1
        
        all_parts.extend(parts)

    return sep.join(all_parts)

