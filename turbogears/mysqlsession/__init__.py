# -*- coding: UTF-8 -*-
#
# Pasirasyk.lt
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Session classes

from datetime import datetime
try:
    import cPickle as pickle
except ImportError:
    import pickle
from file_fields.widgets.file_field import File

from turbogears import config
from cherrypy.filters.sessionfilter import RamStorage

from model import SOMySQLSessionStorage

class MySQLSession:
    """Class for storing session information in the MySQL backend.

        >>> from turbogears import config
        >>> config.update({'sqlobject.dburi': 'sqlite:///:memory:'})

    To use this backend call

        >>> MySQLSession.init()

    The backend will change
        
        >>> 'MySQLSession' in repr(config.get('session_filter.storage_class',
        ...     None))
        True

    And a new table 'session_storage' will be created

        >>> from model import SOMySQLSessionStorage
        >>> SOMySQLSessionStorage._connection.tableExists(SOMySQLSessionStorage.sqlmeta.table)
        True
        >>> SOMySQLSessionStorage.sqlmeta.table
        'session_storage'

    """

    ram_storage = RamStorage()

    @classmethod
    def init(cls):
        config.update({'session_filter.storage_class': cls})
        SOMySQLSessionStorage.createTable(ifNotExists=True)

    def save(self, id, data, expiration_time):
        """Save the session data and the expiration time for that session id"""
        old_session = SOMySQLSessionStorage.selectBy(sid=id)

        to_pickle = {}
        to_ram = {}
        for k, v in data.iteritems():
            if isinstance(v, File):
                # All unpickleable items should go here. Note: these objects
                # will be erased during the next server restart
                to_ram[k] = v
            else:
                to_pickle[k] = v

        self.ram_storage.save(id, to_ram, expiration_time)

        pickled_data = pickle.dumps(to_pickle)
        if old_session.count() > 0:
            session = old_session.getOne()
            session.sid = id
            session.data = pickled_data
            session.expiration_time = expiration_time
        else:
            session = SOMySQLSessionStorage(sid=id,
                data=pickled_data,
                expiration_time=expiration_time)

    def load(self, id):
        """Load and return session data"""
        try:
            session = SOMySQLSessionStorage.selectBy(sid=id).getOne()
            data = pickle.loads(session.data)
            try:
                # If the server was reloaded the data could disappear. But we
                # warned you about this above
                data.update(self.ram_storage.load(id)[0])
            except TypeError:
                pass
            return (data, session.expiration_time)
        except:
            return None

    def clean_up(self, session):
        """Clean up expired sessions"""
        expired = SOMySQLSessionStorage.select(
            SOMySQLSessionStorage.q.expiration_time < datetime.now())
        for s in expired:
            session.on_delete_session(s.sid)
            s.destroySelf()
