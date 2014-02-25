from five import grok
from plone import api

from plone.app.layout.navigation.interfaces import INavigationRoot


class AppRouter(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('app-router')

    def update(self):
        self.next_url = self._get_redirector()

    def render(self):
        return self.request.response.redirect(self.next_url)

    def _get_redirector(self):
        portal = api.portal.get()
        portal_url = portal.absolute_url()
        if not api.user.is_anonymous():
            return portal_url
        else:
            return portal_url + '/de'
