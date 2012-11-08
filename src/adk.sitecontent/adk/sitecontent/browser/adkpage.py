from zope.interface import implements, Interface
from Acquisition import aq_inner, aq_parent
from AccessControl import Unauthorized
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

from adk.sitecontent import sitecontentMessageFactory as _


class IADKPageView(Interface):
    """
    ADKPage view interface
    """
    
    def parent_info():
        """ Back to parent link implementation respecting the custom folder implementation"""


class ADKPageView(BrowserView):
    """
    ADKPage browser view
    """
    implements(IADKPageView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def parent_info(self):
        """
        Query parent information in order to construct back to overview links.
        """
        context = aq_inner(self.context)
        portal_url = getToolByName(context, 'portal_url')
        portal_membership = getToolByName(context, 'portal_membership')
        checkPermission = portal_membership.checkPermission
        # Check if we are at the site root
        if IPloneSiteRoot.providedBy(context):
            return None
        # Get the parent and try to catch potential unauthorized exceptions
        parent = aq_parent(context)
        try:
            if getattr(parent, 'getId', None) is None or parent.getId() == 'talkback':
                parent = aq_parent(aq_inner(parent))
            if not checkPermission('List folder contents', parent):
                return None
            return[dict(title=parent.Title(),
                        url=parent.absolute_url())]
    
        except Unauthorized:
            return None
