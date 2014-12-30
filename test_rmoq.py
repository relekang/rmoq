# -*- coding: utf-8 -*-
import os
import shutil
import unittest
import requests
from datetime import datetime

import rmoq


def timer(func, *args):
    start_time = datetime.now()
    result = func(*args)
    end_time = datetime.now()
    return end_time - start_time, result


class MockTestCase(unittest.TestCase):
    def tearDown(self):
        directories = [os.path.join(os.getcwd(), 'fixtures'), os.path.join(os.getcwd(), 'path')]
        for directory in directories:
            if os.path.exists(directory):
                shutil.rmtree(directory)

    def assert_response(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code)
        self.assertGreater(len(response.text), 100)
        self.assertEqual(response.headers['content-type'], 'text/html; charset=utf-8')

    def test_rmoq_decorator(self):
        @rmoq.activate()
        def perform_requests():
            first_timedelta, first_response = timer(requests.get, 'http://rolflekang.com')
            self.assertTrue(
                os.path.exists(os.path.join(os.getcwd(), 'fixtures/rolflekang.com.txt'))
            )
            last_timedelta, last_response = timer(requests.get, 'http://rolflekang.com')
            self.assertGreater(first_timedelta, last_timedelta)
            self.assert_response(first_response)
            self.assert_response(last_response)

        perform_requests()
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), 'fixtures/rolflekang.com.txt')))

    def test_rmoq_decorator_with_path(self):
        @rmoq.activate('path')
        def perform_requests():
            requests.get('http://rolflekang.com/feed.xml')

        perform_requests()
        self.assertTrue(
            os.path.exists(os.path.join(os.getcwd(), 'path/rolflekang.com_feed.xml.txt'))
        )

    def test_with_statements(self):
        with rmoq.Mock():
            requests.get('http://rolflekang.com/feed.xml')
        self.assertTrue(
            os.path.exists(os.path.join(os.getcwd(), 'fixtures/rolflekang.com_feed.xml.txt'))
        )
        with rmoq.Mock('path'):
            requests.get('http://rolflekang.com/feed.xml')
        self.assertTrue(
            os.path.exists(os.path.join(os.getcwd(), 'path/rolflekang.com_feed.xml.txt'))
        )

    def test_get_filename(self):
        self.assertEqual(rmoq.Mock._get_filename('http://rolflekang.com'), 'rolflekang.com.txt')
        self.assertEqual(rmoq.Mock._get_filename('http://rolflekang.com/'), 'rolflekang.com.txt')
        self.assertEqual(rmoq.Mock._get_filename('http://rolflekang.com/feed.xml'),
                         'rolflekang.com_feed.xml.txt')
