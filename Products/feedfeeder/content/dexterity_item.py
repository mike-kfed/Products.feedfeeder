from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.feedfeeder import _
#from example.conference.session import ISession
from five import grok
from plone.app.textfield import RichText
#from plone.directives import form
from plone.autoform import directives as form
#from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.indexer import indexer
from plone.supermodel import model
import plone.app.textfield
from zope import schema
from zope.component import createObject
from zope.event import notify
from zope.filerepresentation.interfaces import IFileFactory
from zope.interface import invariant, Invalid
from zope.lifecycleevent import ObjectCreatedEvent

from zope import interface
from plone.dexterity import content


import datetime

def updatedDefaultValue():
    return datetime.datetime.today()

class IDexterityFeedfeederItem(model.Schema):
    """A conference program. Programs can contain Sessions.
    """

    feed_item_author = schema.TextLine(
        title=_(u"Feed Item Author"),
        required=False,
    )

    feed_item_updated = schema.Datetime(
        title=_(u"Feed Item Updated"),
        required=False,
        defaultFactory=updatedDefaultValue,
    )

    text = plone.app.textfield.RichText(
        title=_(u"Text"),
        required=False,
    )

    link = schema.URI(
        title=_(u"Link"),
        required=False,
    )

    feed_title = schema.TextLine(
        title=_(u"Feed Title"),
        required=False,
    )

    media_name = schema.TextLine(
        title=_(u"Media Name"),
        required=False,
    )

    media_type = schema.TextLine(
        title=_(u"Media Type"),
        required=False,
    )

class DexterityFeedfeederItem(content.Item):

    interface.implements(IDexterityFeedfeederItem)

    #def getURL(self):
    #    return self.link

    def getFeedTitle(self):
        return self.title
    def getFeedItemAuthor(self):
        return self.feed_item_author
    def getFeedItemUpdated(self):
        return self.feed_item_updated
    def getLink(self):
        return self.link
    def getHasBody(self):
        return self.text and len(self.text) > 0
    def getObjectids(self):
        return []
    def getMedianame(self):
        return self.media_name
    def getMediatype(self):
        return self.media_type

    @property
    def getObjectInfo(self):
        """hack, apparently objectInfo is a hidden field in the archetype implementation"""
        return None

    def setObjectInfo(self, value):
        """original implementation stores the feed data returned from feedparser"""
        return None

# Views

class DexterityFeedfeederItemView(grok.View):
    grok.context(IDexterityFeedfeederItem)
    grok.require('zope2.View')

    def sessions(self):
        """Return a catalog search result of sessions to show
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(object_provides=ISession.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_order='sortable_title')
