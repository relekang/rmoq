import codecs
import re
from os import path

from setuptools import find_packages, setup


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding="utf-8").read()


with open("rmoq/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

setup(
    name="rmoq",
    version=version,
    url="http://github.com/relekang/rmoq",
    author="Rolf Erik Lekang",
    author_email="me@rolflekang.com",
    description="A simple request-mocker that will download",
    long_description=read("README.rst"),
    packages=find_packages(exclude="tests"),
    install_requires=[
        "mock",
        "requests",
    ],
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
