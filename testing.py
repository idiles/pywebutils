#
# Utilities for code testing
# Copyright (c) 2008 IDILES SYSTEMS, UAB
# All rights reserved.
#

import sys

def setupsa():
    """Setup environment for SQLAlchemy-based tests.
    """
    from elixir import metadata, session, setup_all
    metadata.bind = 'sqlite:///:memory:'
    setup_all(create_tables=True)

def setupdf():
    """Setup Dragonfly ESB configuration.
    """
    setupsa()

    from idileslib.soa import ServiceProxy
    ServiceProxy.load_locations('/opt/idiles/dragonfly/webservices/testing.conf')

