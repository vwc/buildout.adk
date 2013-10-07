from five import grok

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
