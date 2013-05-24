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

from plone.app.contentlisting.interfaces import IContentListing

from adk.contentpages.contentblock import IContentBlock

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
        self.has_blocks = len(self.contentblocks()) > 0

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
