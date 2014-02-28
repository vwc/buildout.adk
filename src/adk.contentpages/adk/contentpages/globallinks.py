from Acquisition import aq_inner
from five import grok
from plone import api

from zope.interface import Interface
from zope.component import getMultiAdapter

from plone.app.layout.viewlets.interfaces import IPortalFooter
from adk.contentpages.sectionfolder import ISectionFolder


class GlobalLinksViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('adk.contentpages.GlobalLinksViewlet')
    grok.viewletmanager(IPortalFooter)

    def update(self):
        self.portal_url = api.portal.get().absolute_url()

    def get_root_url(self):
        context = aq_inner(self.context)
        nav_root = api.portal.get_navigation_root(context)
        if nav_root:
            return nav_root.absolute_url()
        else:
            return api.portal.get().absolute_url()

    def section_folders(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name="portal_catalog")
        nav_root = api.portal.get_navigation_root(context)
        items = catalog(object_provides=ISectionFolder.__identifier__,
                        path=dict(query='/'.join(nav_root.getPhysicalPath()),
                                  depth=1),
                        review_state='published',
                        sort_on='getObjPositionInParent')
        return items

    def current_language(self):
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        lang = portal_state.language()
        return lang

    def de_in_path(self):
        context = aq_inner(self.context)
        item_in_path = False
        if 'de' in context.getPhysicalPath():
            item_in_path = True
        return item_in_path
