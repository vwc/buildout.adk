from random import randint
from five import grok
from plone import api

from zope.interface import Interface

from plone.app.layout.viewlets.interfaces import IPortalFooter
from plone.app.contentlisting.interfaces import IContentListing
from adk.testimonials.testimonial import ITestimonial


class CustomerQuotesViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('adk.testimonials.CustomerQuotesViewlet')
    grok.viewletmanager(IPortalFooter)

    def update(self):
        self.portal_url = api.portal.get().absolute_url()
        self.has_quotes = len(self.quotes()) > 0

    def selected_quote(self):
        brains = self.quotes()
        return brains[randint(0, len(brains)-1)]

    def quotes(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        brains = catalog(object_provides=ITestimonial.__identifier__,
                         review_state='published')
        quotes = IContentListing(brains)
        return quotes
