"""Definition of the ADKFolder content type
"""

from zope.interface import implements, directlyProvides

try:
    from Products.LinguaPlone.public import *
except ImportError:
    from Products.Archetypes.atapi import * # No LinguaPlone support
#from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
#from plone.app.folder import folder

from adk.sitecontent import sitecontentMessageFactory as _
from adk.sitecontent.interfaces import IADKFolder
from adk.sitecontent.config import PROJECTNAME

ADKFolderSchema = folder.ATFolderSchema.copy() + Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ADKFolderSchema['title'].storage = AnnotationStorage()
ADKFolderSchema['description'].storage = AnnotationStorage()

schemata.finalizeATCTSchema(
    ADKFolderSchema,
    folderish=True,
    moveDiscussion=False
)

class ADKFolder(folder.ATFolder):
    """A dedicated folder content type with automatic listings"""
    implements(IADKFolder)

    meta_type = "ADKFolder"
    schema = ADKFolderSchema

    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

registerType(ADKFolder, PROJECTNAME)
