rmoq |frigg| |coverage| |version|
=================================

A simple request mocker that caches requests responses to files.

Installation
------------

Install it with pip: ::

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



More advanced usage can be found in the `documentation`_.

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

.. _`documentation`: http://rmoq.readthedocs.org/en/latest/
