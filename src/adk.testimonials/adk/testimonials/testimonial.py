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


class ITestimonial(form.Schema, IImageScaleTraversable):
    """
    A sinlge customer statement
    """
    title = schema.TextLine(
        title=_(u"Fullname"),
        required=False,
    )
    country = schema.TextLine(
        title=_(u"Country"),
        required=False,
    )
    text = RichText(
        title=_(u"Statement"),
        required=True,
    )


class Testimonial(Container):
    grok.implements(ITestimonial)


class View(grok.View):
    """ sample view class """

    grok.context(ITestimonial)
    grok.require('zope2.View')
    grok.name('view')
