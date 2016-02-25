# -*- coding: utf-8 -*-

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='changelog',
    version='0.1.0',
    author='Jonas Kalderstam',
    author_email='jonas@kalderstam.se',
    description='Changelog generator based on git commit messages or github issues',
    license='MIT',
    keywords='changelog,version,git,github',
    url='https://github.com/spacecowboy/changelog-writer',
    packages=['changelog'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Documentation"],
    install_requires=[
        "pytoml"],
    package_data={
        "changelog": [
            "../README.md",
            "../LICENSE",
            "../config.toml"]})
