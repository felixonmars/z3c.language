##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

"""
$Id$
"""
__docformat__ = 'restructuredtext'

import unittest

import zope.component
from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite

from z3c.language.negotiator import testing
from z3c.language.negotiator import app
from z3c.language.negotiator import testing


class NegotiatorBaseTest(testing.BaseTestINegotiator):

    def getTestClass(self):
        return app.Negotiator


class NegotiatorTest(zope.component.testing.PlacelessSetup, 
    unittest.TestCase):

    def setUp(self):
        super(NegotiatorTest, self).setUp()
        self.negotiator = app.Negotiator()
        zope.component.provideAdapter(testing.LanguageSessionStub)

    def test_policy(self):
        default = 'session --> browser --> server'
        self.assertEqual(self.negotiator.policy, default)
        self.negotiator.policy = 'server'
        self.assertEqual(self.negotiator.policy, 'server')

    def test_serverLanguage(self):
        self.assertEqual(self.negotiator.serverLanguage, u'en')
        self.negotiator.serverLanguage = u'de'
        self.assertEqual(self.negotiator.serverLanguage, u'de')

    def test_offeredLanguages(self):
        self.assertEqual(self.negotiator.offeredLanguages, [])
        self.negotiator.offeredLanguages = [u'de', u'en']
        self.assertEqual(self.negotiator.offeredLanguages, [u'de', u'en'])

    def test_getLanguages(self):
        # first set the default policy to 'browser'
        self.negotiator.policy = 'browser'
        self.assertEqual(self.negotiator.policy, 'browser')

        _cases = (
            (('en','de'), ('en','de','fr'),  'en'),
            (('en'),      ('it','de','fr'),  None),
            (('pt-br','de'), ('pt_BR','de','fr'),  'pt_BR'),
            (('pt-br','en'), ('pt', 'en', 'fr'),  'pt'),
            (('pt-br','en-us', 'de'), ('de', 'en', 'fr'),  'en'),
            )

        for user_pref_langs, obj_langs, expected in _cases:
            env = testing.EnvStub(user_pref_langs)
            self.assertEqual(self.negotiator.getLanguage(obj_langs, env),
                             expected)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(NegotiatorBaseTest),
        unittest.makeSuite(NegotiatorTest),
        DocFileSuite('README.txt',
                     setUp=testing.doctestSetUp,
                     tearDown=testing.doctestTearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                     ),
                           ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
