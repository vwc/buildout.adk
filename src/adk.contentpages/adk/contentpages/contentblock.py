from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from plone import api
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

from plone.app.contentlisting.interfaces import IContentListing

from adk.contentpages.contentbox import IContentBox

from adk.contentpages import MessageFactory as _


display_options = SimpleVocabulary([
    SimpleTerm(value=u'left', title=_(u'Sidebar Left')),
    SimpleTerm(value=u'right', title=_(u'Sidebar Right')),
    SimpleTerm(value=u'split', title=_(u'Split View')),
    SimpleTerm(value=u'full', title=_(u'Full View'))]
)


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
    blockDisplay = schema.Choice(
        title=_(u"Block Layout"),
        vocabulary=display_options,
        required=False,
    )


class ContentBlock(dexterity.Container):
    grok.implements(IContentBlock)


class View(grok.View):
    grok.context(IContentBlock)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_boxes = len(self.contentboxes()) > 0

    def parentpage_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def parentpage_title(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.Title()

    def contentboxes(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        blocks = catalog(object_provides=IContentBox.__identifier__,
                         path=dict(query='/'.join(context.getPhysicalPath()),
                                   depth=1),
                         review_state='published',
                         sort_on='getObjPositionInParent')
        results = IContentListing(blocks)
        return results

    def can_edit(self):
        return not api.user.is_anonymous()

    def get_column_class(self, col):
        context = aq_inner(self.context)
        selected = getattr(context, 'blockDisplay', '')
        if col == selected:
            klass = '8'
        else:
            klass = '4'
        return klass


class ContentView(grok.View):
    grok.context(IContentBlock)
    grok.require('zope2.View')
    grok.name('content-view')

    def update(self):
        self.has_boxes = len(self.contentboxes()) > 0

    def contentboxes(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        blocks = catalog(object_provides=IContentBox.__identifier__,
                         path=dict(query='/'.join(context.getPhysicalPath()),
                                   depth=1),
                         review_state='published',
                         sort_on='getObjPositionInParent')
        results = IContentListing(blocks)
        return results

    def get_column_class(self, col):
        context = aq_inner(self.context)
        selected = getattr(context, 'blockDisplay', '')
        if col == selected:
            klass = '8'
        else:
            klass = '4'
        return klass
