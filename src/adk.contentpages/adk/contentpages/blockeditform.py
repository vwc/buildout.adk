from five import grok
from plone import api
from Acquisition import aq_inner
from zope import schema

from zope.schema import getFieldsInOrder
from zope.component import getUtility
from zope.lifecycleevent import modified

from plone.directives import form
from z3c.form import button

from plone.app.textfield import RichText

from plone.dexterity.interfaces import IDexterityFTI
from Products.statusmessages.interfaces import IStatusMessage
from adk.contentpages.contentpage import IContentBlock

from adk.contentpages import MessageFactory as _


class IBlockEdit(form.Schema):

    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )
    text = RichText(
        title=_(u"Content Block Body"),
        required=False,
    )


class BlockEditForm(form.SchemaEditForm):
    grok.context(IContentBlock)
    grok.require('cmf.AddPortalContent')
    grok.name('edit-content-block')

    schema = IBlockEdit
    ignoreContext = False
    css_class = 'overlayForm popover-form'

    label = _(u"Edit content block")

    def updateActions(self):
        super(BlockEditForm, self).updateActions()
        self.actions['save'].addClass("btn btn-primary")
        self.actions['cancel'].addClass("btn btn-default")

    @button.buttonAndHandler(_(u"Edit content block"), name="save")
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

    def getContent(self):
        context = aq_inner(self.context)
        fti = getUtility(IDexterityFTI, name='adk.contentpages.contentblock')
        schema = fti.lookupSchema()
        fields = getFieldsInOrder(schema)
        data = {}
        for key, value in fields:
            data[key] = getattr(context, key, value)
        data['title'] = context.Title()
        return data

    def applyChanges(self, data):
        context = aq_inner(self.context)
        item = context
        fti = getUtility(IDexterityFTI, name='adk.contentpages.contentblock')
        schema = fti.lookupSchema()
        fields = getFieldsInOrder(schema)
        for key, value in fields:
            try:
                new_value = data[key]
                setattr(context, key, new_value)
            except KeyError:
                continue
        modified(item)
        item.reindexObject(idxs='modified')
        IStatusMessage(self.request).addStatusMessage(
            _(u"The content block has successfully been updated"),
            type='info')
        next_url = item.absolute_url()
        return self.request.response.redirect(next_url)
