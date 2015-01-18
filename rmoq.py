# -*- coding: utf-8 -*-
import os
import re
import six
import requests

from requests.packages.urllib3 import HTTPResponse

if six.PY3:
    from unittest import mock
    from io import BytesIO as BufferIO

    def prepare_for_write(value, encoding='utf-8', errors='replace'):
        if isinstance(value, bytes):
            return value.decode(encoding=encoding, errors=errors)
        return value

else:
    import mock
    from six import StringIO as BufferIO

    def prepare_for_write(value, encoding='utf-8', errors='replace'):
        if isinstance(value, unicode):
            return value.encode(encoding=encoding, errors=errors)
        return unicode(value, errors=errors).encode(encoding=encoding, errors=errors)


class Mock(object):
    path = 'fixtures'

    def __init__(self, path=None):
        if path:
            self.path = path

    def __enter__(self):
        def on_send(session, request, *args, **kwargs):
            return self.on_request(session, request, *args, **kwargs)

        self.patch = mock.patch('requests.Session.send', on_send)
        self.patch.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.patch.stop()

    def activate(self, path=None):
        if path is not None:
            if isinstance(path, six.string_types):
                self.path = path

        def activate(func):
            if isinstance(func, type):
                return self._decorate_class(func)

            def wrapper(*args, **kwargs):
                with self:
                    return func(*args, **kwargs)

            return wrapper

        return activate

    def _decorate_class(self, cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, self.activate()(getattr(cls, attr)))
        return cls

    def on_request(self, session, request, *args, **kwargs):
        response_path = os.path.join(os.getcwd(), self.path, self._get_filename(request.url))

        if os.path.exists(response_path):
            content_type, content = self._read_body_from_file(response_path)
            response = HTTPResponse(
                status=200,
                body=BufferIO(content),
                preload_content=False,
                headers={'Content-Type': content_type}
            )
            adapter = session.get_adapter(request.url)
            response = adapter.build_response(request, response)
        else:
            self.patch.stop()
            response = requests.get(request.url)
            self.patch.start()
            self._write_body_to_file(response_path, response.text, response.headers['Content-Type'])

        return response

    @staticmethod
    def _get_filename(url):
        return '{}.txt'.format(re.sub(r'/$', '', re.sub(r'https?://', '', url)).replace('/', '_'))

    @staticmethod
    def _read_body_from_file(path):
        with open(path) as f:
            content = f.read()
            content_type = content.split('\n')[0]
            content = '\n'.join(content.split('\n')[1:])
            return content_type, content.encode('utf-8', 'replace')

    @staticmethod
    def _write_body_to_file(path, content, content_type):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'w') as f:
            f.write('{}\n'.format(content_type))
            f.write(prepare_for_write(content))


_mock = Mock()

__all__ = []
for __attr in (a for a in dir(_mock)):
    __all__.append(__attr)
    globals()[__attr] = getattr(_mock, __attr)
