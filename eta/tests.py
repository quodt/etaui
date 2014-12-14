# -*- coding: utf-8 -*-
import doctest
import os
import unittest


project_root = os.path.dirname(os.path.dirname(__file__))
here = os.path.dirname(__file__)

test_dir = os.path.join(here, 'testing')
conf = os.path.join(test_dir, 'testing.ini')
default_app = None


def setUp(test):
    pass


def tearDown(test):
    pass


def create_suite(testfile, layer=None, level=None,
                 tearDown=tearDown, setUp=setUp, cls=doctest.DocFileSuite,
                 encoding='utf-8'):
    suite = cls(
        testfile, tearDown=tearDown, setUp=setUp,
        optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        encoding=encoding)
    if layer:
        suite.layer = layer
    if level:
        suite.level = level
    return suite


def test_suite():
    s = unittest.TestSuite((
        create_suite('protocol.rst'),
    ))
    return s
