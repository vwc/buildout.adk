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
    form.fieldset(
        'settings',
        label=_(u"Display Settings"),
        fields=['featured', 'selected_layout']
    )
    featured = schema.Bool(
        title=_(u"Featured Block"),
        description=_(u"Mark as featured to visually highlight this block"),
        required=False,
    )
    selected_layout = schema.TextLine(
        title=_(u"Selected Layout"),
        description=_(u"User selected layout for display as string"),
        required=False
    )


alsoProvides(IDisplaySettings, IFormFieldProvider)
