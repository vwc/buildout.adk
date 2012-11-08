"""Definition of the ADKPage content type
"""

from zope.interface import implements, directlyProvides

try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.atapi import * # No LinguaPlone support
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
# Import ImageField from plone.app.blob
from plone.app.blob.field import ImageField as BlobAwareImageField

from adk.sitecontent import sitecontentMessageFactory as _
from adk.sitecontent.interfaces import IADKPage
from adk.sitecontent.config import PROJECTNAME

ADKPageSchema = schemata.ATContentTypeSchema.copy() + Schema((

    # -*- Your Archetypes field definitions here ... -*-

    BlobAwareImageField(
        'image',
        storage=AnnotationStorage(),
        widget=ImageWidget(
            label=_(u"Preview Image"),
            description=_(u"Upload an image that will be displayed as a preview image in listings and search results."),
        ),
        validators=('isNonEmptyFile'),
    ),


    TextField(
        'text',
        searchable=True,
        default_output_type='text/x-html-safe',
        storage=AnnotationStorage(),
        widget=RichWidget(
            label=_(u"Text"),
            description=_(u""),
            allow_file_upload=False,
            rows=25,
        ),
        required=True,
        validators=('isTidyHtmlWithCleanup'),
    ),
    
    BooleanField('tableContents',
        required=False,
        languageIndependent=True,
        widget=BooleanWidget(
            label=_(u'help_enable_table_of_contents',
                    default=u'Table of contents'),
            description=_(u'help_enable_table_of_contents_description',
                    default=u'If selected, this will show a table of contents at the top of the page.')
            ),
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

ADKPageSchema['title'].storage = AnnotationStorage()
ADKPageSchema['description'].storage = AnnotationStorage()

schemata.finalizeATCTSchema(ADKPageSchema, moveDiscussion=False)

class ADKPage(base.ATCTContent):
    """A lingua plone aware documents providing preview images."""
    implements(IADKPage)

    meta_type = "ADKPage"
    schema = ADKPageSchema

    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    image = ATFieldProperty('image')

    text = ATFieldProperty('text')
    
    # Utilize the default Plone ATNewsItem image API
    # to provide scaled images for folder listings.
    
    def tag(self, **kwargs):
        """Generate image tag using the ImageField API"""
        return self.getField('image').tag(self, **kwargs)
    
    def __bobo_traverse__(self, REQUEST, name):
        """Transparent access to image scales by travering to image_<scalename>"""
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                return image
        
        return super(ADKPage, self).__bobo_traverse__(REQUEST, name)
    


registerType(ADKPage, PROJECTNAME)
