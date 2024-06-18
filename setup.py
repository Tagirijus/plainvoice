#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages

setup(
    name="plainvoice",
    version="0.0.1",
    author="Manuel Senfft",
    author_email="info@tagirijus.de",
    description="Creating invoices and quotes with a plaintext mindset.",
    license="MIT",
    keywords="invoice invoice-generator quote quote-generator",
    packages=find_packages(),
    install_requires=[
        'click>=8.1.7,<9.0.0',
        'rich>=13.7.1,<14.0.0',
        'prompt_toolkit>=3.0.45,<4.0.0'
    ],
)
