# -*- coding: utf-8 -*-
from .base import Mock
from rmoq.backends import FileStorageBackend, RmoqBackend


_mock = Mock()

__all__ = [
    RmoqBackend,
    FileStorageBackend,
]
for __attr in (a for a in dir(_mock)):
    __all__.append(__attr)
    globals()[__attr] = getattr(_mock, __attr)
