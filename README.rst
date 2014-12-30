rmoq
====

|frigg|

A simple request mocker that caches requests responses to files.

Installation
------------

Install it from pip with: ::

    pip install rmoq

Usage
-----

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


It can also be used in a with statement ::

    def test_remote_call():
        with rmoq.Mock():
            response = requests.get('http://example.com')
            assert response.body == 'Example'

The mock object can also take a path as an argument.


----------------------

MIT © Rolf Erik Lekang


.. |frigg| image:: https://ci.frigg.io/badges/relekang/rmoq/
    :target: https://ci.frigg.io/relekang/rmoq/last/

