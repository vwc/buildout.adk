from Acquisition import aq_inner
from five import grok
from plone import api
from plone.directives import dexterity, form

from zope import schema

from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.textfield import RichText

from plone.app.contentlisting.interfaces import IContentListing

from adk.contentpages.contentblock import IContentBlock
from adk.contentpages.contentbox import IContentBox

from adk.contentpages import MessageFactory as _


class IContentPage(form.Schema, IImageScaleTraversable):
    """
    Content page with automatic subcontent listing
    """
    displayTitle = schema.TextLine(
        title=_(u"Display Title"),
        description=_(u"Alternative Title for displaying alternative "
                      u"headline"),
        required=False,
    )
    pageTitle = schema.TextLine(
        title=_(u"Page Title"),
        description=_(u"First headline of the page body"),
        required=False,
    )
    pageTeaser = schema.Text(
        title=_(u"Page Teaser"),
        description=_(u"Enter a sumamry or teaser text"),
        required=False,
    )
    text = RichText(
        title=_(u"Body Text"),
        required=False,
    )


class ContentPage(dexterity.Container):
    grok.implements(IContentPage)


class View(grok.View):
    grok.context(IContentPage)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_content = len(self.context.items()) > 0
        self.has_blocks = len(self.contentblocks()) > 0
        self.has_boxes = len(self.contentboxes()) > 0

    def subcontent(self):
        if self.has_blocks:
            items = self.contentblocks()
            results = {'item_type': 'blocks',
                       'items': IContentListing(items)}
        else:
            items = self.contentpages()
            results = {'item_type': 'pages',
                       'items': IContentListing(items)}
        return results

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

    def contentblocks(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        blocks = catalog(object_provides=IContentBlock.__identifier__,
                         path=dict(query='/'.join(context.getPhysicalPath()),
                                   depth=1),
                         review_state='published',
                         sort_on='getObjPositionInParent')
        return blocks

    def contentpages(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')
        items = catalog(object_provides=IContentPage.__identifier__,
                        path=dict(query='/'.join(context.getPhysicalPath()),
                                  depth=1),
                        review_state='published',
                        sort_on='getObjPositionInParent')
        return items

    def get_contentblock(self, obj):
        ctx = obj.getObject()
        tmpl = ctx.restrictedTraverse('@@content-view')()
        return tmpl

    def can_edit(self):
        return not api.user.is_anonymous()
