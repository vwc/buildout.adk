from five import grok
from plone import api

from plone.app.layout.navigation.interfaces import INavigationRoot


class Imprint(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('imprint-view')


class ContactInfo(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('contact-view')


class TermsAndConditions(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('terms-and-conditions')
