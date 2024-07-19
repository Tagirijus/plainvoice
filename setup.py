#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages

_setup = setup(
    name='plainvoice',
    version='0.0.1',
    author='Manuel Senfft',
    author_email='info@tagirijus.de',
    description='Creating invoices and documents with a plaintext mindset.',
    license='MIT',
    keywords='invoice invoice-generator quote quote-generator',
    packages=find_packages(),
    install_requires=[
        'click~=8.1',
        'jinja2~=3.1',
        'rich~=13.7',
        'weasyprint~=62',
        'PyYAML~=6.0'
    ],
)
