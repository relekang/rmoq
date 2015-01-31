# -*- coding: utf-8 -*-
import six

string_types = six.string_types
StringIO = six.StringIO

if six.PY3:
    from unittest import mock  # noqa
    from io import BytesIO
    StringIO = BytesIO

    def prepare_for_write(value, encoding='utf-8', errors='replace'):
        if isinstance(value, bytes):
            return value.decode(encoding=encoding, errors=errors)
        return value

    def read_file(f):
        content = f.read()
        content_type = content.split('\n')[0]
        content = '\n'.join(content.split('\n')[1:])
        return content_type, content.encode('utf-8', 'replace')

else:
    import mock  # noqa
    _text_type = unicode  # noqa

    def prepare_for_write(value, encoding='utf-8', errors='replace'):
        if isinstance(value, _text_type):
            return value.encode(encoding=encoding, errors=errors)
        return _text_type(value, errors=errors).encode(encoding=encoding, errors=errors)

    def read_file(f):
        content = f.read()
        content_type = content.split('\n')[0]
        content = '\n'.join(content.split('\n')[1:])
        return content_type, content
