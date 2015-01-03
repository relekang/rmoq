rmoq
====

|frigg| |coverage| |version| |downloads|

A simple request mocker that caches requests responses to files.

Installation
------------

Install it with pip: ::

    pip install rmoq

Usage
-----

**Function decorator**

The example below will put the content of fixtures/example.com.txt
into the body of the request and if it does not exist the content
will be downloaded and stored in fixtures/example.com.txt. ::

    @rmoq.activate()
    def test_remote_call():
        response = requests.get('http://example.com')
        assert response.body == 'Example'


The example below works as the one above it just uses the given path
(test_fixtures) instead of the default path. ::

    @rmoq.activate('test_fixtures')
    def test_remote_call():
        response = requests.get('http://example.com')
        assert response.body == 'Example'


**With statements**

It can also be used in a with statement ::

    def test_remote_call():
        with rmoq.Mock():
            response = requests.get('http://example.com')
            assert response.body == 'Example'

The mock object can also take a path as an argument.

**Class decorator**

The decorator will also work for classes, which means you can decorate a whole test-case: ::

    @rmoq.activate()
    class RemoteTestCase(unittest.TestCase)
        def test_remote_call():
            response = requests.get('http://example.com')
            assert response.body == 'Example'


----------------------

MIT © Rolf Erik Lekang


.. |frigg| image:: https://ci.frigg.io/badges/relekang/rmoq/
    :target: https://ci.frigg.io/relekang/rmoq/last/

.. |coverage| image:: https://ci.frigg.io/badges/coverage/relekang/rmoq/
    :target: https://ci.frigg.io/relekang/rmoq/last/

.. |version| image:: https://pypip.in/version/rmoq/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/rmoq/
    :alt: Latest Version

.. |downloads| image:: https://pypip.in/download/rmoq/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/rmoq/
    :alt: Downloads
