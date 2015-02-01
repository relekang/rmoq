Backends
--------

rmoq supports custom storage backends by passing an instance into the backend parameter of
:func:`rmoq.activate` method. A storage backend must inherit from :class:`rmoq.RmoqStorageBackend`
and implement the :func:`.get` and :func:`.put` methods.

.. autoclass:: rmoq.RmoqStorageBackend
    :members:

.. autoclass:: rmoq.FileStorageBackend
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: rmoq.MemcachedStorageBackend
    :members:
    :undoc-members:
    :show-inheritance:
