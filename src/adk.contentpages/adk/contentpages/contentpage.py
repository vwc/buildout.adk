from Acquisition import aq_inner
from five import grok
from plone import api
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from adk.contentpages import MessageFactory as _


class IContentPage(form.Schema, IImageScaleTraversable):
    """
    Content page with automatic subcontent listing
    """
    displayTitle = schema.TextLine(
        title=_(u"Display Title"),
        description=_(u"Alternative Title for displaying alternative "
                      u"headline"),
        required=True,
    )
    text = RichText(
        title=_(u"Body Text"),
        required=True,
    )


class ContentPage(dexterity.Container):
    grok.implements(IContentPage)


class View(grok.View):
    grok.context(IContentPage)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_content = len(self.context.items()) > 0
