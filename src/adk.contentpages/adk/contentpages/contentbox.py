from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from adk.contentpages import MessageFactory as _

icon_klass = SimpleVocabulary([
    SimpleTerm(value=u'fa-info', title=_(u'Info')),
    SimpleTerm(value=u'fa-film', title=_(u'Video')),
    SimpleTerm(value=u'fa-picture', title=_(u'Image')),
    SimpleTerm(value=u'fa-thumbs-up', title=_(u'Thumbs Up!')),
    SimpleTerm(value=u'fa-warning-sign', title=_(u'Attention')),
    SimpleTerm(value=u'fa-time', title=_(u'Time')),
    SimpleTerm(value=u'fa-download', title=_(u'Download'))]
)


class IContentBox(form.Schema, IImageScaleTraversable):
    """
    A sinlge content panel or box
    """
    text = RichText(
        title=_(u"Box Content Body"),
        required=False,
    )
    selected_icon = schema.Choice(
        title=_(u"Selected Icon"),
        description=_(u"Box Heading Icon"),
        vocabulary=icon_klass,
        default='fa-info',
        required=False
    )


class ContentBox(Container):
    grok.implements(IContentBox)


class View(grok.View):
    grok.context(IContentBox)
    grok.require('zope2.View')
    grok.name('view')

    def parentpage_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def parentpage_title(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.Title()
