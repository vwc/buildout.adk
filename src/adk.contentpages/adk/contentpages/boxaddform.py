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
from adk.contentpages.contentblock import IContentBlock

from adk.contentpages import MessageFactory as _


class IBoxAdd(form.Schema):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )
    description = schema.Text(
        title=_(u"Introduction"),
        required=False,
    )
    text = RichText(
        title=_(u"Content Block Body"),
        required=False,
    )


class BoxAddForm(form.SchemaEditForm):
    grok.context(IContentBlock)
    grok.require('cmf.AddPortalContent')
    grok.name('add-content-box')

    schema = IBoxAdd
    ignoreContext = True
    css_class = 'overlayForm popover-form'

    label = _(u"Add new content box")

    def updateActions(self):
        super(BoxAddForm, self).updateActions()
        self.actions['save'].addClass("btn btn-primary")
        self.actions['cancel'].addClass("btn btn-link")

    @button.buttonAndHandler(_(u"Add content bbox"), name="save")
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
            'adk.contentpages.contentbox',
            checkConstraints=True, **data)
        modified(item)
        item.reindexObject(idxs='modified')
        IStatusMessage(self.request).addStatusMessage(
            _(u"New item has successfully been added"),
            type='info')
        next_url = item.absolute_url()
        return self.request.response.redirect(next_url)


class MainBoxAddForm(form.SchemaEditForm):
    grok.context(IContentPage)
    grok.require('cmf.AddPortalContent')
    grok.name('add-content-box')

    schema = IBoxAdd
    ignoreContext = True
    css_class = 'overlayForm popover-form'

    label = _(u"Add new content box")

    def updateActions(self):
        super(MainBoxAddForm, self).updateActions()
        self.actions['save'].addClass("btn btn-primary")
        self.actions['cancel'].addClass("btn btn-link")

    @button.buttonAndHandler(_(u"Add content bbox"), name="save")
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
            'adk.contentpages.contentbox',
            checkConstraints=True, **data)
        modified(item)
        item.reindexObject(idxs='modified')
        IStatusMessage(self.request).addStatusMessage(
            _(u"New item has successfully been added"),
            type='info')
        next_url = item.absolute_url()
        return self.request.response.redirect(next_url)
