from zope.interface import alsoProvides
from zope import schema
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider

from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from adk.contentpages import MessageFactory as _

display_options = SimpleVocabulary([
    SimpleTerm(value=u'left', title=_(u'Sidebar Left')),
    SimpleTerm(value=u'right', title=_(u'Sidebar Right')),
    SimpleTerm(value=u'split', title=_(u'Split View')),
    SimpleTerm(value=u'full', title=_(u'Full View'))]
)


class IDisplaySettings(form.Schema):
    """
       Marker/Form interface for DisplaySettings
    """
    form.fieldset(
        'settings',
        label=_(u"Display Settings"),
        fields=['featured', 'blockDisplay']
    )
    featured = schema.Bool(
        title=_(u"Featured Block"),
        description=_(u"Mark as featured to visually highlight this block"),
        required=False,
    )
    blockDisplay = schema.Choice(
        title=_(u"Block Layout"),
        vocabulary=display_options,
        default='left',
        required=False,
    )


alsoProvides(IDisplaySettings, IFormFieldProvider)
