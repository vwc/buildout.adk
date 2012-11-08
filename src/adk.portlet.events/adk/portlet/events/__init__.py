from zope.i18nmessageid import MessageFactory
ADKEventPortletMessageFactory = MessageFactory('adk.portlet.events')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
