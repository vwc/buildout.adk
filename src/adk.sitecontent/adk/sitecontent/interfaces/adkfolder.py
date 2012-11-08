from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from adk.sitecontent import sitecontentMessageFactory as _

class IADKFolder(Interface):
    """A dedicated folder content type with automatic listings"""
    
    # -*- schema definition goes here -*-
