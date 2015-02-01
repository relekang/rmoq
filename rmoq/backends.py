# -*- coding: utf-8 -*-
import os
import re

from . import compat


class RmoqStorageBackend(object):
    """
    Base backend for rmoq backends. All storage backends for rmoq must inherit this
    backend if it is to be used with rmoq.
    """

    def get(self, prefix, url):
        """
        Fetches a request response from storage. Should be overridden by subclasses.

        :param prefix: A prefix that separates containers of request responses in the storage.
        :param url: The url of the request.
        """
        raise NotImplementedError

    def put(self, prefix, url, content, content_type):
        """
        Writes a request response in to storage. Should be overridden by subclasses.

        :param prefix: A prefix that separates containers of request responses in the storage.
        :param url: The url of the request.
        :param content: The content of the request response.
        :param content_type: The content type header of the request response.
        """
        raise NotImplementedError

    @staticmethod
    def _parse(content):
        return (
            compat.make_str(content.split('\n')[0]),
            compat.make_str('\n'.join(content.split('\n')[1:]))
        )

    @staticmethod
    def clean_url(url, replacement='_'):
        """
        Cleans the url for protocol prefix and trailing slash and replaces special characters
        with the given replacement.

        :param url: The url of the request.
        :param replacement: A string that is used to replace special characters.
        """
        cleaned = re.sub(r'/$', '', re.sub(r'https?://', '', url))
        for character in '/ _ ? & : ; %'.split():
            cleaned = cleaned.replace(character, replacement)
        return cleaned


class FileStorageBackend(RmoqStorageBackend):
    """
    A rmoq backend that reads and writes to the local file system.
    This is the default backend.
    """

    def get(self, prefix, url):
        filename = self.get_filename(prefix, url)
        if os.path.exists(filename):
            with open(filename) as f:
                return compat.read_file(f)

    def put(self, prefix, url, content, content_type):
        filename = self.get_filename(prefix, url)

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, mode='w') as f:
            f.writelines([content_type, '\n', compat.prepare_for_write(content)])

    def get_filename(self, prefix, url):
        """
        Creates a file path on the form: current-working-directory/prefix/cleaned-url.txt

        :param prefix: The prefix from the .get() and .put() methods.
        :param url: The url of the request.
        :return: The created path.
        """
        return '{}.txt'.format(os.path.join(os.getcwd(), prefix, self.clean_url(url)))


class MemcachedStorageBackend(RmoqStorageBackend):
    """
    Storage backend for rmoq that uses memcached for storage. Takes a the same arguments
    as python-memcached: a list of servers and options as keyword arguments.
    """

    def __init__(self, servers, **options):
        import memcache

        self.client = memcache.Client(servers=servers, **options)

    def get(self, prefix, url):
        return self._parse(self.client.get(self.create_key(prefix, url)))

    def put(self, prefix, url, content, content_type):
        return self.client.add(
            self.create_key(prefix, url),
            '\n'.join([content_type, content]),
            60 * 60 * 24
        )

    def create_key(self, *parts):
        return ''.join([self.clean_url(part, '') for part in parts])
