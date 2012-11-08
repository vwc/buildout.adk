from zope.interface import implements, Interface

from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from adk.sitecontent.interfaces import IADKPage
from adk.sitecontent.interfaces import IADKFolder
from adk.sitecontent import sitecontentMessageFactory as _


class IAdkFolderView(Interface):
    """
    adklisting view interface
    """
    
    def has_pages():
        """ Test for pages availability"""

    def pages():
        """ List of containes subpages """


class AdkFolderView(BrowserView):
    """
    adklisting browser view
    """
    implements(IAdkFolderView)
    
    pagelist_template = ViewPageTemplateFile('adklisting.pt')
    folderlist_template = ViewPageTemplateFile('adkfolderlisting.pt')
        
    def __call__(self):
        """Use the __call__ method to provide the view templates dynamically"""
        if self.has_one_page() == True:
            next_url = self.getFirstPageUrl()
            self.request.response.redirect(next_url)
            return ''
        if self.has_subfolders():
            return self.folderlist_template()
        else:
            return self.pagelist_template()
    
    def has_subfolders(self):
        return len(self.subfolders()) > 0
    
    def has_one_page(self):
        return len(self.pages()) == 1
    
    def has_pages(self):
        return len(self.pages()) > 0

    def pages(self):
        """
        Query the catalog for containes ADKPages by their interface
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        return [dict(title=page.Title,
                     description=page.Description,
                     url=page.getURL(),
                     text=page.getObject().getText(),
                     image_tag=page.getObject().tag(scale='thumb', css_class='tileImage'))
                for page in catalog(object_provides=IADKPage.__identifier__,
                                    path=dict(query='/'.join(context.getPhysicalPath()),
                                              depth=1),
                                    sort_on='getObjPositionInParent',
                                    review_state='published',
                                    )
                ]
    
    def first_page(self):
        """If we only have one page inside this folder we show all the details
        of the page including the body text"""
        context= aq_inner(self.context)
        has_pages = self.has_pages()
        if has_pages == None:
            return None
        else:
            pages = self.pages()
            first_page = pages[0]
            return first_page
    
    def getFirstPageUrl(self):
        """
        If we only have one ADKPage in this folder we redirect to it.
        This function provides the url.
        """
        context = aq_inner(self.context)
        pages = self.pages()
        first_page = pages[0]
        first_page_url = first_page['url']
        return first_page_url
    
    def subfolders(self):
        """A list of potential subfolders"""
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        return [dict(title=folder.Title,
                     description=folder.Description,
                     url=folder.getURL())
                for folder in catalog(object_provides=IADKFolder.__identifier__,
                                      path=dict(query='/'.join(context.getPhysicalPath()),
                                                depth=1),
                                      sort_on='getObjPositionInParent',
                                      review_state='published')
                ]
