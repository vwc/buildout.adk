from five import grok
from plone import api
from Acquisition import aq_inner
from zope import schema
from zope.lifecycleevent import modified

from plone.directives import form
from z3c.form import button

from plone.app.textfield import RichText

from plone.dexterity.utils import createContentInContainer
from Products.statusmessages.interfaces import IStatusMessage
from adk.contentpages.contentpage import IContentPage

from adk.contentpages import MessageFactory as _


class IBlockAdd(form.Schema):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )
    subtitle = schema.TextLine(
        title=_(u"Subtitle"),
        description=_(u"Optional extra information displayed along the "
                      u"section title"),
        required=False,
    )
    text = RichText(
        title=_(u"Content Block Body"),
        required=False,
    )


class BlockAddForm(form.SchemaEditForm):
    grok.context(IContentPage)
    grok.require('cmf.AddPortalContent')
    grok.name('add-content-block')

    schema = IBlockAdd
    ignoreContext = True
    css_class = 'overlayForm popover-form'

    label = _(u"Add new content block")

    def updateActions(self):
        super(BlockAddForm, self).updateActions()
        self.actions['save'].addClass("btn btn-primary")
        self.actions['cancel'].addClass("btn btn-default")

    @button.buttonAndHandler(_(u"Add content block"), name="save")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)

    @button.buttonAndHandler(_(u"cancel"))
    def handleCancel(self, action):
        context = aq_inner(self.context)
        msg = _(u"Process has been cancelled."),
        api.portal.show_message(message=msg, request=self.request)
        return self.request.response.redirect(context.absolute_url())

    def applyChanges(self, data):
        context = aq_inner(self.context)
        container = context
        item = createContentInContainer(
            container,
            'adk.contentpages.contentblock',
            checkConstraints=True, **data)
        modified(item)
        item.reindexObject(idxs='modified')
        IStatusMessage(self.request).addStatusMessage(
            _(u"A new job opening has successfully been added"),
            type='info')
        next_url = item.absolute_url()
        return self.request.response.redirect(next_url)
