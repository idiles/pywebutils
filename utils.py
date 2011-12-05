#
# Idiles Library
# Copyright (c) 2008 IDILES SYSTEMS, UAB
# All rights reserved.
#

from datetime import datetime

dtformat = '%Y-%m-%d %H:%M:%S'
dateformat = '%Y-%m-%d'

def strptime(dt, format):
    """Alternative for datetime.strptime() when using python 2.4."""
    import time
    return datetime(*(time.strptime(dt, format)[0:6]))

def parse_date(date):
    """Parse ISO format date string into Datetime object.
    
        >>> from datetime import datetime
        >>> parse_date('2007-10-05') == datetime(2007, 10, 5)
        True
        >>> parse_date('2007-10-05 08:12:43') == datetime(2007, 10, 5)
        True
        >>> parse_date('2007-10-06') == datetime(2007, 10, 5)
        False
        >>> print parse_date('invalid')
        None
    """
    date = date.split(' ')[0]
    try:
        year, month, day = date.split('-')[:3]
        year = int(year)
        month = int(month)
        day = int(day)
    except:
        return None
    return datetime(year, month, day)


def parse_datetime(date):
    """Parse ISO format date/time string into Datetime object.
    
        >>> from datetime import datetime
        >>> print parse_datetime('2007-10-05')
        None
        >>> parse_datetime('2007-10-05 08:12:43') == datetime(2007, 10, 5, 8, 12, 43)
        True
        >>> parse_datetime('2007-10-06') == datetime(2007, 10, 5)
        False
        >>> print parse_datetime('invalid')
        None
    """
    try:
        date, time = date.split(' ')
        year, month, day = date.split('-')[:3]
        year = int(year)
        month = int(month)
        day = int(day)
        hours, minutes, seconds = time.split(':')[:3]
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        return datetime(year, month, day, hours, minutes, seconds)
    except:
        return None
