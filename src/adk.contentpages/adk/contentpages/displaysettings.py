from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from adk.contentpages import MessageFactory as _


class IDisplaySettings(form.Schema):
    """
       Marker/Form interface for DisplaySettings
    """
    # -*- Your Zope schema definitions here ... -*-


alsoProvides(IDisplaySettings, IFormFieldProvider)
