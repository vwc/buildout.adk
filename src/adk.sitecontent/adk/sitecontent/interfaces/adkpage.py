from zope import schema
from zope.interface import Interface

from adk.sitecontent import sitecontentMessageFactory as _


class IADKPage(Interface):
    """A lingua plone aware documents providing preview images."""

    # -*- schema definition goes here -*-
    image = schema.Bytes(
        title=_(u"Preview Image"),
        required=False,
        description=_(u"Upload an image that will be displayed as a preview "
                      u"image in listings and search results."),
    )

    text = schema.SourceText(
        title=_(u"Text"),
        required=True,
        description=_(u"Field description"),
    )
