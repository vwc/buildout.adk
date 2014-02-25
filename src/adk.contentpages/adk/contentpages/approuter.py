from five import grok
from plone import api

from plone.app.layout.navigation.interfaces import INavigationRoot


class AppRouter(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('app-router')

    def render(self):
        portal = api.portal.get()
        portal_url = portal.absolute_url()
        next_url = portal_url + '/de'
        if not api.user.is_anonymous():
            next_url = portal_url
        return self.request.response.redirect(next_url)
