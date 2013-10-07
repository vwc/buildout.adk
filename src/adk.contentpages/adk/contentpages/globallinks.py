from five import grok
from plone import api

from zope.interface import Interface

from plone.app.layout.viewlets.interfaces import IPortalFooter


class GlobalLinksViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('adk.contentpages.GlobalLinksViewlet')
    grok.viewletmanager(IPortalFooter)

    def update(self):
        self.portal_url = api.portal.get().absolute_url()
