# -*- coding: utf-8 -*-
import re
import ast

from setuptools import setup, find_packages


_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('pir/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="pip-require",
    version=version,
    description=(
        "Depending on the installation or uninstall packages, "
        "and then edit the requirements file."
    ),
    license="MIT",
    author="kk6",
    author_email="hiro.ashiya@gmail.com",
    url="https://github.com/kk6/pip-require",
    packages=find_packages(),
    install_requires=[
        "Click",
    ],
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities"
    ],
    entry_points="""
        [console_scripts]
        pir = pir.cli:cli
    """
)
