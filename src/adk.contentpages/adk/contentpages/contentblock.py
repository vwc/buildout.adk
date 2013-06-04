from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from adk.contentpages import MessageFactory as _


class IContentBlock(form.Schema, IImageScaleTraversable):
    """
    A blcok of content usable inside a content page.
    """
    subtitle = schema.TextLine(
        title=_(u"Subtitle"),
        description=_(u"Optional extra information displayed along the "
                      u"section title"),
        required=False,
    )
    text = RichText(
        title=_(u"Content Block Body"),
        required=False,
    )


class ContentBlock(dexterity.Container):
    grok.implements(IContentBlock)


class View(grok.View):
    grok.context(IContentBlock)
    grok.require('zope2.View')
    grok.name('view')


class ContentView(grok.View):
    grok.context(IContentBlock)
    grok.require('zope2.View')
    grok.name('content-view')
