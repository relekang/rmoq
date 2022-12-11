# -*- coding: utf-8 -*-
import os
import shutil
import unittest
from datetime import datetime

import requests

import rmoq
from rmoq.backends import FileStorageBackend


def timer(func, *args):
    start_time = datetime.now()
    result = func(*args)
    end_time = datetime.now()
    return end_time - start_time, result


class BaseTestCase(unittest.TestCase):
    def tearDown(self):  # noqa
        directories = [
            os.path.join(os.getcwd(), "fixtures"),
            os.path.join(os.getcwd(), "path"),
        ]
        for directory in directories:
            if os.path.exists(directory):
                shutil.rmtree(directory)


class MockTestCase(BaseTestCase):
    def assert_response(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code)
        self.assertGreater(len(response.text), 100)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")

    def test_rmoq_decorator(self):
        @rmoq.activate()
        def perform_requests():
            first_timedelta, first_response = timer(
                requests.get, "http://rolflekang.com"
            )
            self.assertTrue(
                os.path.exists(os.path.join(os.getcwd(), "fixtures/rolflekang.com.txt"))
            )
            last_timedelta, last_response = timer(requests.get, "http://rolflekang.com")
            self.assertGreater(first_timedelta, last_timedelta)
            self.assert_response(first_response)
            self.assert_response(last_response)

        perform_requests()
        self.assertTrue(
            os.path.exists(os.path.join(os.getcwd(), "fixtures/rolflekang.com.txt"))
        )

    def test_disabled_by_environ(self):
        os.environ["RMOQ_DISABLED"] = "True"

        @rmoq.activate()
        def perform_requests():
            requests.get("http://rolflekang.com")

        perform_requests()
        self.assertFalse(
            os.path.exists(os.path.join(os.getcwd(), "fixtures/rolflekang.com.txt"))
        )
        del os.environ["RMOQ_DISABLED"]

    def test_rmoq_decorator_with_args(self):
        @rmoq.activate("path", FileStorageBackend())
        def perform_requests():
            requests.get("http://rolflekang.com/feed.xml")

        perform_requests()
        self.assertTrue(
            os.path.exists(
                os.path.join(os.getcwd(), "path/rolflekang.com_feed.xml.txt")
            )
        )

    def test_with_statements(self):
        with rmoq.Mock():
            requests.get("http://rolflekang.com/feed.xml")
        self.assertTrue(
            os.path.exists(
                os.path.join(os.getcwd(), "fixtures/rolflekang.com_feed.xml.txt")
            )
        )
        with rmoq.Mock("path"):
            requests.get("http://rolflekang.com/feed.xml")
        self.assertTrue(
            os.path.exists(
                os.path.join(os.getcwd(), "path/rolflekang.com_feed.xml.txt")
            )
        )

    def test_class_decorator(self):
        @rmoq.activate()
        class A(object):
            def perform_requests(self):
                requests.get("http://rolflekang.com")

        a = A()
        self.assertTrue(isinstance(a, A))
        a.perform_requests()
        self.assertTrue(
            os.path.exists(os.path.join(os.getcwd(), "fixtures/rolflekang.com.txt"))
        )


class BackendTestCase(BaseTestCase):
    def test_get_filename(self):
        self.assertEqual(
            rmoq.RmoqStorageBackend.clean_url("http://rolflekang.com"), "rolflekang.com"
        )
        self.assertEqual(
            rmoq.RmoqStorageBackend.clean_url("http://rolflekang.com/"),
            "rolflekang.com",
        )
        self.assertEqual(
            rmoq.RmoqStorageBackend.clean_url("http://rolflekang.com/feed.xml"),
            "rolflekang.com_feed.xml",
        )
        self.assertEqual(
            rmoq.RmoqStorageBackend.clean_url("http://rolflekang.com/?get&parameters"),
            "rolflekang.com__get_parameters",
        )

    def test__parse(self):
        self.assertEqual(
            rmoq.RmoqStorageBackend._parse("1\n2\n3\n4\n"), ("1", "2\n3\n4\n")
        )


class BackendTestMixin(object):
    backend = rmoq.RmoqStorageBackend()

    def test_storage(self):
        self.backend.put(
            "fixtures", "http://rolflekang.com", "1\n2\n3\n4\n", "content-type"
        )
        content = self.backend.get("fixtures", "http://rolflekang.com")
        self.assertIsNotNone(content)
        self.assertEqual(content[1], "1\n2\n3\n4\n")
        self.assertEqual(content[0], "content-type")


class FileStorageBackendTestCase(BackendTestMixin, BaseTestCase):
    backend = rmoq.FileStorageBackend()


class MemcachedStorageBackendTestCase(BackendTestMixin, BaseTestCase):
    backend = rmoq.MemcachedStorageBackend(["127.0.0.1:11211"])

    def setUp(self) -> None:
        super().setUp()
        print(len(self.backend.client.get_stats()))
        if len(self.backend.client.get_stats()) == 0:
            raise unittest.SkipTest("Memcached is not running")
