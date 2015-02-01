# -*- coding: utf-8 -*-
from .base import Mock
from rmoq.backends import FileStorageBackend, RmoqStorageBackend, MemcachedStorageBackend


_mock = Mock()

__all__ = [
    RmoqStorageBackend,
    FileStorageBackend,
    MemcachedStorageBackend,
]
for __attr in (a for a in dir(_mock)):
    __all__.append(__attr)
    globals()[__attr] = getattr(_mock, __attr)
