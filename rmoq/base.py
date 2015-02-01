# -*- coding: utf-8 -*-
import ast
import os

import requests
from requests.packages.urllib3 import HTTPResponse

from . import compat
from .backends import FileStorageBackend, RmoqStorageBackend


class Mock(object):
    """
    The mocker class that mocks requests in rmoq. It supports being used in with-statements
    and have a method :method:`activate` that can be used as a decorator on functions or classes.
    """

    def __init__(self, prefix='fixtures', backend=FileStorageBackend()):
        self.prefix = prefix
        self.backend = backend

    def __enter__(self):
        def on_send(session, request, *args, **kwargs):
            return self.on_request(session, request, *args, **kwargs)

        if not self.disabled:
            self.patch = compat.mock.patch('requests.Session.send', on_send)
            self.patch.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.disabled:
            self.patch.stop()

    @property
    def disabled(self):
        return ast.literal_eval(os.environ.get('RMOQ_DISABLED', 'False'))

    def activate(self, prefix=None, backend=None):
        """
        A decorator used to activate the mocker.

        :param prefix:
        :param backend: An instance of a storage backend.
        """
        if isinstance(prefix, compat.string_types):
            self.prefix = prefix

        if isinstance(backend, RmoqStorageBackend):
            self.backend = backend

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

        content = self.backend.get(self.prefix, request.url)
        if content is not None:
            response = HTTPResponse(
                status=200,
                body=compat.create_response_body(content[1]),
                preload_content=False,
                headers={'Content-Type': content[0]}
            )
            adapter = session.get_adapter(request.url)
            response = adapter.build_response(request, response)
        else:
            self.patch.stop()
            response = requests.get(request.url)
            self.patch.start()
            self.backend.put(
                self.prefix,
                request.url,
                response.text,
                response.headers['Content-Type']
            )

        return response
