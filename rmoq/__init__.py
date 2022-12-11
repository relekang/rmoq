# -*- coding: utf-8 -*-
from rmoq.backends import FileStorageBackend, MemcachedStorageBackend, RmoqStorageBackend

from .base import Mock

__version__ = "0.4.2"

_mock = Mock()

__all__ = [
    __version__,
    RmoqStorageBackend,
    FileStorageBackend,
    MemcachedStorageBackend,
]
for __attr in (a for a in dir(_mock)):
    __all__.append(__attr)
    globals()[__attr] = getattr(_mock, __attr)
