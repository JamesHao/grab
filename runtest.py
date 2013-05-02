#!/usr/bin/env python
# coding: utf-8
import unittest
import sys
from optparse import OptionParser
import logging

from test.util import prepare_test_environment, clear_test_environment
import test.util
from grab.tools.watch import watch

TEST_CASE_LIST = (
    'test.base_interface',
    'test.post_feature',
    'test.grab_proxy',
    'test.upload_file',
    'test.limit_option',
    'test.cookies',
    'test.response_class',
    'test.charset_issue',
    # test server
    'test.fake_server',
    # tools
    'test.text_tools',
    'test.lxml_tools',
    'test.tools_account',
    'test.tools_control',
    # extension sub-system
    'test.extension',
    # extensions
    'test.text_extension',
    'test.lxml_extension',
    'test.form_extension',
    'test.doc_extension',
    # test items
    'test.item',
    # test selector
    'test.selector',
    # idn
    'test.i18n',
    # flask
    #'test.test_flask',
)


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = OptionParser()
    parser.add_option('-t', '--test', help='Run only specified tests')
    parser.add_option('--transport', help='Test specified transport',
                      default='curl.CurlTransport')
    opts, args = parser.parse_args()

    test.util.GRAB_TRANSPORT = opts.transport

    prepare_test_environment()
    # Check tests integrity
    # Ensure that all test modules are imported correctly
    for path in TEST_CASE_LIST:
        __import__(path, None, None, ['foo'])

    loader = unittest.TestLoader()
    if opts.test:
        suite = loader.loadTestsFromName(opts.test)
    else:
        suite = loader.loadTestsFromNames(TEST_CASE_LIST)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    clear_test_environment()
    if result.wasSuccessful():
        return 0
    else:
        return -1


if __name__ == '__main__':
    watch()
    main()
