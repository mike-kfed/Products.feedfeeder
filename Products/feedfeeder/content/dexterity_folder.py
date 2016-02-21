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
from z3c.form.browser.textlines import TextLinesFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.component import createObject
from zope.event import notify
from zope.filerepresentation.interfaces import IFileFactory
from zope.interface import invariant, Invalid
from zope.lifecycleevent import ObjectCreatedEvent
import datetime


class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")


class IDexterityFeedfeederFolder(model.Schema):
    """A conference program. Programs can contain Sessions.
    """
    title = schema.TextLine(
        title=_(u"Feed Title"),
    )

    description = schema.Text(
        title=_(u"Feed description"),
    )

    feeds = schema.Text(
        title=_(u"Feeds"),
        description=u"List of rss feeds. You can prefix feed link titles using | separator. It is probably a good idea to add a colon or dash at the end of the prefix ('My place: |http://myplace/feed').",
        required=False,
    )


    form.widget(redirect='plone.app.z3c.form.browser.radio import RadioFieldWidget')
    redirect = schema.Bool(
        title=_(u"Automatic redirect of feed items"),
        description=u"If checked the feed item will be automatically redirected if you don't have the edit permission.",
        default=False,
        required=True,
    )

    # TODO: implement
    default_transition = schema.Choice(
        title=_(u"Default transition"),
        description=u"When updating this feed's item the transition selected below will be performed.",
        required=False,
        vocabulary=u"plone.app.vocabularies.WorkflowTransitions",
    )

# Views

class View(grok.View):
    grok.context(IDexterityFeedfeederFolder)
    grok.require('zope2.View')

    def sessions(self):
        """Return a catalog search result of sessions to show
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(object_provides=ISession.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_order='sortable_title')
