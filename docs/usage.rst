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



**Disable in one test run**
Setting the environment variable `RMOQ_DISABLED` to `True` will disable rmoq: ::

    $ RMOQ_DISABLED=True py.test

This can be useful to make sure that the a CI server does not use time on saving new fixtures if you
are only using fixtures locally.
