rmoq
====

|frigg|

A simple request mocker that caches requests to files.


Usage
-----

The example below will put the content of fixtures/example.com
into the body of the request and if it does not exist. ::

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


----------------------

MIT © Rolf Erik Lekang


.. |frigg| image:: https://ci.frigg.io/badges/relekang/rmoq/
    :target: https://ci.frigg.io/relekang/rmoq/last/

