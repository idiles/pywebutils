# -*- coding: UTF-8 -*-
#
# Kiveda.lt
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# MySQL session storage classes


from sqlobject import SQLObject, StringCol, UnicodeCol, DateTimeCol

from turbogears.database import PackageHub

hub = PackageHub('')
__connection__ = hub

class SOMySQLSessionStorage(SQLObject):
    class sqlmeta:
        table = 'session_storage'

    sid = StringCol(length=40, alternateID=True)
    data = StringCol()
    expiration_time = DateTimeCol()


