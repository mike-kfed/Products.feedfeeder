import unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from Products.feedfeeder.content.dexterity_folder import IDexterityFeedfeederFolder
from Products.feedfeeder.content.dexterity_item import IDexterityFeedfeederItem
from Products.feedfeeder.testing import INTEGRATION_TESTING

class MockDexterityFeedfeederFolder(object):
    pass

class TestProgramIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_adding(self):
        self.folder.invokeFactory('Products.feedfeeder.dexterity_folder', 'dfeedfold')
        p1 = self.folder['dfeedfold']
        self.assertTrue(IDexterityFeedfeederFolder.providedBy(p1))

    def test_adding_item(self):
        self.folder.invokeFactory('Products.feedfeeder.dexterity_folder', 'dfeedfold')
        p1 = self.folder['dfeedfold']

        p1.invokeFactory('Products.feedfeeder.dexterity_item', 'dfeeditem')
        i1 = p1['dfeeditem']
        self.assertTrue(IDexterityFeedfeederItem.providedBy(i1))

    def test_getting_item_info(self):
        self.folder.invokeFactory('Products.feedfeeder.dexterity_folder', 'dfeedfold2')
        p1 = self.folder['dfeedfold2']
        p1.feeds = "http://deinemama.com"
        self.assertTrue(len(p1.feeds.split("\n")) == 1)
        self.assertTrue(len(p1.getFeeds()) == 1)
        p1.invokeFactory('Products.feedfeeder.dexterity_item', 'dfeeditem')
        i1 = p1['dfeeditem']
        self.assertTrue(p1.getItem('dfeeditem') is not None)
        self.assertTrue(p1.getItem('dfeeditem_nonexist') is None)
        i1.media_name = 'web'
        i1.reindexObject()
        self.assertEqual(i1.media_name, 'web')

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

# run it with ./bin/test Products.feedfeeder
