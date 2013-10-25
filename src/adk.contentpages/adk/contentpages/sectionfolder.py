from Acquisition import aq_inner
from five import grok
from plone import api
from plone.directives import dexterity, form

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.app.contentlisting.interfaces import IContentListing

from adk.contentpages.contentpage import IContentPage


class ISectionFolder(form.Schema, IImageScaleTraversable):
    """
    A folder acting as navigation root
    """


class SectionFolder(dexterity.Container):
    grok.implements(ISectionFolder)


class View(grok.View):
    grok.context(ISectionFolder)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_pages = len(self.contentpages()) > 0

    def page_details(self, index):
        items = self.contentpages()
        return items[index]

    def contentpages(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name="portal_catalog")
        brains = catalog(object_provides=IContentPage.__identifier__,
                         path=dict(query='/'.join(context.getPhysicalPath()),
                                   depth=1),
                         review_state='published',
                         sort_on='getObjPositionInParent')
        results = IContentListing(brains)
        return results
