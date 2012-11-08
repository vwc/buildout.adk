from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.portlets.cache import render_cachekey

from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress


class IADKEventPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IADKEventPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "ADK Event Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    _template = ViewPageTemplateFile('adkeventportlet.pt')
    
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
    
    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())
    
    @property
    def available(self):
        return len(self._data())
    
    def published_events(self):
        return self._data()
    
    @memoize
    def _data(self):
        """Query the catalog for recent events in order to display them on the frontpage."""
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        return catalog(portal_type=['Event', ],
                       end={'query': DateTime(),
                            'range': 'min'},
                       sort_on='start',
                       review_state='published'
                       )[:3]


class AddForm(base.NullAddForm):
    """Portlet add form.
    """
    def create(self):
        return Assignment()

