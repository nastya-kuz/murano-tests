# -*- coding: utf-8 -*-


import unittest2
import json
import logging
from funkload.FunkLoadTestCase import FunkLoadTestCase

logging.basicConfig()
LOG = logging.getLogger(' REST service tests')

class TestSuite(FunkLoadTestCase):

    def setUp(self):
        self.url = self.conf_get('main', 'url')
        self.headers = {'X-Auth-Token': '3685674500ff83eb62b5c5d453e0cacd'}

    def tearDown(self):
        self.headers = {}

    def test_create_environment(self):
        body = '{"name": "Test"}'
        response = self.post(self.url, params=[['headers', self.headers],
                                               ['data', body]])

        LOG.error(response)
        assert response == Null


if __name__ == '__main__':
    unittest2.main()
