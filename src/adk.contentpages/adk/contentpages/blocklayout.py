from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from plone import api

from adk.contentpages.contentblock import IContentBlock


class BlockLayout(grok.View):
    grok.context(IContentBlock)
    grok.require('cmf.ModifyPortalContent')
    grok.name('block-layout')

    def update(self):
        """ Add post form handler here """

    def parentpage_url(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.absolute_url()

    def parentpage_title(self):
        context = aq_inner(self.context)
        parent = aq_parent(context)
        return parent.Title()
