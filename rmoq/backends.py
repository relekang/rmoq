# -*- coding: utf-8 -*-
import os
import re

from . import compat


class RmoqBackend(object):
    """
    Base backend for rmoq backends
    """

    def get(self, prefix, url):
        raise NotImplementedError

    def put(self, prefix, url, content, content_type):
        raise NotImplementedError

    @staticmethod
    def _parse(content):
        return content.split('\n')[0], '\n'.join(content.split('\n')[1:])

    @staticmethod
    def _clean_url(url, replacement='_'):
        cleaned = re.sub(r'/$', '', re.sub(r'https?://', '', url))
        for character in ['/', '_', '?', '&']:
            cleaned = cleaned.replace(character, replacement)
        return cleaned


class FileStorageBackend(RmoqBackend):
    def get(self, prefix, url):
        filename = self._get_filename(prefix, url)
        if os.path.exists(filename):
            with open(filename) as f:
                return compat.read_file(f)

    def put(self, prefix, url, content, content_type):
        filename = self._get_filename(prefix, url)

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, mode='w') as f:
            f.writelines([content_type, '\n', compat.prepare_for_write(content)])

    def _get_filename(self, prefix, url):
        return '{}.txt'.format(os.path.join(os.getcwd(), prefix, self._clean_url(url)))
