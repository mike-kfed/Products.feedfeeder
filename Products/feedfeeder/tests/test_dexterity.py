import unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.dexterity.interfaces import IDexterityFTI

from Products.feedfeeder.content.dexterity_folder import IDexterityFeedfeederFolder
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

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

# run it with ./bin/test Products.feedfeeder
