from Acquisition import aq_inner
from five import grok
from plone import api

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.contentlisting.interfaces import IContentListing

from Products.CMFCore.interfaces import IContentish
from adk.testimonials.testimonial import ITestimonial

from adk.testimonials import MessageFactory as _


class ITestimonials(form.Schema, IImageScaleTraversable):
    """
    Folder to hold testimonials
    """


class Testimonials(Container):
    grok.implements(ITestimonials)


class View(grok.View):
    """ sample view class """

    grok.context(ITestimonials)
    grok.require('zope2.View')
    grok.name('view')


class TestimonialListing(grok.View):
    grok.context(IContentish)
    grok.require('zope2.View')
    grok.name('testimonial-listing')

    def update(self):
        self.has_items = len(self.testimonials()) > 0

    def testimonials(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        results = catalog(object_provides=ITestimonial.__identifier__,
                          review_state='published')
        items = IContentListing(results)
        return items
