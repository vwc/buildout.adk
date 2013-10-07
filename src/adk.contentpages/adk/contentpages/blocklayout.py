from AccessControl import Unauthorized
from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from plone import api

from zope.component import getMultiAdapter

from adk.contentpages.contentblock import IContentBlock

from adk.contentpages import MessageFactory as _


class BlockLayout(grok.View):
    grok.context(IContentBlock)
    grok.require('cmf.ModifyPortalContent')
    grok.name('block-layout')

    def update(self):
        context = aq_inner(self.context)
        self.errors = {}
        if (
            'form.button.LayoutA' in self.request or
            'form.button.LayoutB' in self.request or
            'form.button.LayoutC' in self.request or
            'form.button.LayoutD' in self.request):
            authenticator = getMultiAdapter((context, self.request),
                                            name=u'authenticator')
            if not authenticator.verify():
                raise Unauthorized
            formdata = {}
            formdata['layout'] = self.request.get('form.button', None)
            self._set_layout(formdata)

    def _set_layout(self, data):
        msg = _(u"Your layout selection has been safed")
        api.portal.show_message(msg, request=self.request)
        next_url = self.context.absolute_url()
        return self.request.response.redirect(next_url)

    def parentpage_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def parentpage_title(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.Title()
