# Copyright (c) 2010 gocept gmbh & co. kg
# See also LICENSE.txt

from zope.testing import renormalizing
import doctest
import unittest
import zc.buildout.testing

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('gocept.versions', test)


def test_suite():
    return unittest.TestSuite(doctest.DocFileSuite(
        'README.txt',
        setUp=setUp,
        tearDown=zc.buildout.testing.buildoutTearDown,
        checker=renormalizing.RENormalizing([
            zc.buildout.testing.normalize_path])))

