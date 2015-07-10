import codecs
from os import path

from setuptools import find_packages, setup


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()

setup(
    name='rmoq',
    version='0.4.1',
    url='http://github.com/relekang/rmoq',
    author='Rolf Erik Lekang',
    author_email='me@rolflekang.com',
    description='A simple request-mocker that will download',
    long_description=read('README.rst'),
    packages=find_packages(exclude='tests'),
    install_requires=[
        'mock==1.1.0',
        'six==1.9.0',
        'requests',
    ],
    license='MIT',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ]
)
